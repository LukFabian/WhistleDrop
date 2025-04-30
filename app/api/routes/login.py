from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy import select
from app.models import Journalist
from app.api.deps import WhistleSessionDep
from app.auth.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["login"])

@router.post("/login")
async def login(
    session: WhistleSessionDep,
    email: str = Form(...),
    password: str = Form(...),
):
    result = session.execute(select(Journalist).where(Journalist.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
