from typing import Optional
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, LargeBinary, Boolean, DateTime


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


class RSAPublicKey(Base):
    """Model for the stored RSA public keys."""
    __tablename__ = "rsa_public_keys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    public_key_pem: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)  # PEM-encoded public key
    is_used: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    uploads: Mapped[list['Upload']] = relationship(
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