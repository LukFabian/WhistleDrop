from fastapi import UploadFile, File, HTTPException, APIRouter
from sqlalchemy import select
from uuid import uuid4

from app.models import Upload, RSAPublicKey
from app.api.deps import WhistleSessionDep
from app.api.enryption_utils import generate_aes_key, encrypt_file_with_aes, encrypt_key_with_rsa

router = APIRouter(prefix="/file", tags=["upload"])


@router.post("/upload")
async def upload_file(session: WhistleSessionDep, file: UploadFile = File(...)):
    contents = await file.read()
    aes_key = generate_aes_key()
    nonce, encrypted_file = encrypt_file_with_aes(contents, aes_key)

    # Select one unused RSA public key
    result = session.execute(
        select(RSAPublicKey).where(RSAPublicKey.is_used == False).limit(1)
    )
    rsa_key = result.scalar_one_or_none()

    if not rsa_key:
        raise HTTPException(status_code=500, detail="No unused RSA keys available")

    encrypted_aes_key = encrypt_key_with_rsa(rsa_key.public_key_pem, aes_key)

    # Mark the RSA key as used
    rsa_key.is_used = True

    # Store everything in the Upload model
    upload = Upload(
        upload_id=str(uuid4()),
        encrypted_file_data=nonce + encrypted_file,  # Prepend nonce
        encrypted_aes_key=encrypted_aes_key,
        rsa_public_key=rsa_key
    )

    session.add(upload)
    session.commit()

    return {"status": "success", "upload_id": upload.upload_id}
