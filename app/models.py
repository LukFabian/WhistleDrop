from typing import Optional
from datetime import datetime

from pydantic import EmailStr, BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, LargeBinary, Boolean, DateTime


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class RSAPublicKey(Base):
    """Model for the stored RSA public keys."""
    __tablename__ = "rsa_public_keys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    public_key_pem: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    uploads: Mapped[list["Upload"]] = relationship(
        back_populates="rsa_public_key",
        cascade="all, delete-orphan"
    )


class Upload(Base):
    __tablename__ = "uploads"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    upload_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    encrypted_file_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)  # Store file content here
    encrypted_aes_key: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    rsa_public_key_id: Mapped[int] = mapped_column(ForeignKey("rsa_public_keys.id"), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    rsa_public_key: Mapped['RSAPublicKey'] = relationship(back_populates="uploads")


class RSAPairs(Base):
    __tablename__ = "rsa_key_pairs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    public_key_pem: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)  # PEM-encoded public key
    private_key_pem: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)  # PEM-encoded private key
    is_used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)


class Journalist(Base):
    __tablename__ = "journalists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    email: Mapped[EmailStr] = mapped_column(String(254), unique=True, nullable=False)


class JournalistRegister(BaseModel):
    email: EmailStr
    password: str

    # Define a validator for the password field
    # noinspection PyMethodParameters
    @field_validator("password")
    def check_password(cls, value: str, info: ValidationInfo) -> str:
        # convert the password to a string if it is not already
        value = str(value)
        # check that the password has at least 8 characters, one uppercase letter, one lowercase letter, and one digit
        if len(value) < 8:
            raise ValueError("Password must have at least 8 characters")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must have at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must have at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must have at least one digit")
        return value
