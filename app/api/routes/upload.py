from typing import List

from fastapi import UploadFile, File, HTTPException, APIRouter
from sqlalchemy import select
from uuid import uuid4

from app.models import Upload, RSAPublicKey, RSAPairs
from app.api.deps import WhistleSessionDep, JournalistSessionDep
from app.api.enryption_utils import generate_aes_key, encrypt_file_with_aes, encrypt_key_with_rsa, decrypt_key_with_rsa, \
    decrypt_file_with_aes

router = APIRouter(prefix="/file", tags=["upload"])


@router.post("/upload")
async def upload_file(session: WhistleSessionDep, file: UploadFile = File(...)):
    contents = await file.read()
    aes_key = generate_aes_key()
    nonce, encrypted_file = encrypt_file_with_aes(contents, aes_key)

    # Select one unused RSA public key (i.e., one not used in any Upload)
    result = session.execute(
        select(RSAPublicKey)
        .where(~RSAPublicKey.uploads.any())  # No uploads referencing this key
        .limit(1)
    )
    rsa_key = result.scalar_one_or_none()

    if not rsa_key:
        raise HTTPException(status_code=500, detail="No unused RSA keys available")

    encrypted_aes_key = encrypt_key_with_rsa(rsa_key.public_key_pem, aes_key)

    upload = Upload(
        upload_id=str(uuid4()),
        encrypted_file_data=nonce + encrypted_file,
        encrypted_aes_key=encrypted_aes_key,
        rsa_public_key=rsa_key,
        original_filename=file.filename
    )

    session.add(upload)
    session.commit()

    return {"status": "success", "upload_id": upload.upload_id}


@router.get("/uploads")
async def get_my_uploads(
        whistle_session: WhistleSessionDep,
        journalist_session: JournalistSessionDep,
):
    result = whistle_session.execute(
        select(RSAPublicKey)
        .where(RSAPublicKey.uploads.any())  # uploads referencing this key
    )
    rsa_public_keys: List[RSAPublicKey] = result.scalars().all()

    matching_uploads = []

    for key in rsa_public_keys:
        upload_result = whistle_session.execute(
            select(Upload).where(Upload.rsa_public_key_id == key.id)
        )
        uploads: List[Upload] = upload_result.scalars().all()
        res = journalist_session.execute(select(RSAPairs).where(RSAPairs.public_key_pem == key.public_key_pem))
        pair = res.scalar_one_or_none()
        for upload in uploads:
            # Decrypt AES key
            try:
                aes_key = decrypt_key_with_rsa(pair.private_key_pem.decode("utf-8"), upload.encrypted_aes_key)
                # Decrypt file data
                nonce = upload.encrypted_file_data[:12]  # Assuming 12 byte nonce
                encrypted_file = upload.encrypted_file_data[12:]
                file_contents = decrypt_file_with_aes(nonce, encrypted_file, aes_key)

                matching_uploads.append({
                    "upload_id": upload.upload_id,
                    "filename": upload.original_filename or f"decrypted_{upload.upload_id}.bin",
                    "decrypted_preview": file_contents[:100].decode(errors="ignore"),
                    "download_url": f"/file/download/{upload.upload_id}"
                })
            except Exception as e:
                # Skip files we can't decrypt
                print(f"Decryption failed: {e}")
                continue

    return matching_uploads
