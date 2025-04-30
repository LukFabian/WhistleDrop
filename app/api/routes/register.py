from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.models import Journalist, JournalistRegister
from app.api.deps import WhistleSessionDep
from app.auth.security import get_password_hash

router = APIRouter(prefix="/auth", tags=["register"])


@router.post("/register")
async def register_journalist(payload: JournalistRegister,session: WhistleSessionDep):
    # Check for existing user
    result = session.execute(select(Journalist).where(Journalist.email == payload.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    journalist = Journalist(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        is_active=False  # must be activated manually/admin
    )

    session.add(journalist)
    session.commit()
    return {"detail": "Registration successful. Await admin activation."}
