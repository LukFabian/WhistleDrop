from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO

from sqlalchemy import select

from app.api.deps import WhistleSessionDep, JournalistSessionDep
from app.api.enryption_utils import decrypt_key_with_rsa, decrypt_file_with_aes
from app.models import Upload, RSAPairs

router = APIRouter(prefix="/file", tags=["download"])


@router.get("/download/{upload_id}")
async def download_file(upload_id: str, whistle_session: WhistleSessionDep, journalist_session: JournalistSessionDep):
    upload = whistle_session.execute(
        select(Upload).where(Upload.upload_id == upload_id)
    ).scalar_one_or_none()

    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    public_key_pem = upload.rsa_public_key.public_key_pem

    key_pair = journalist_session.execute(
        select(RSAPairs).where(RSAPairs.public_key_pem == public_key_pem)
    ).scalar_one_or_none()

    if not key_pair:
        raise HTTPException(status_code=500, detail="Private key for decryption not found")

    private_key_pem = key_pair.private_key_pem.decode()
    aes_key = decrypt_key_with_rsa(private_key_pem, upload.encrypted_aes_key)

    nonce = upload.encrypted_file_data[:12]
    ciphertext = upload.encrypted_file_data[12:]
    decrypted_data = decrypt_file_with_aes(nonce, ciphertext, aes_key)

    # ✅ Use stored filename, fallback if None
    filename = upload.original_filename or f"decrypted_{upload.upload_id}.bin"

    return StreamingResponse(
        BytesIO(decrypted_data),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
