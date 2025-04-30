from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.api.deps import WhistleSessionDep
from sqlalchemy import select

from app.core.config import settings
from app.models import Journalist

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

async def get_current_journalist(session: WhistleSessionDep = Depends(), token: str = Depends(oauth2_scheme)) -> Journalist:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = session.execute(select(Journalist).where(Journalist.email == email))
    journalist = result.scalar_one_or_none()

    if journalist is None:
        raise credentials_exception

    return journalist