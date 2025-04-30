"""create uploads table

Revision ID: e08f2d4643f4
Revises: 0001_create_rsa_public_keys
Create Date: 2025-04-25 14:12:49.305336

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = '0002_create_uploads'
down_revision = '0001_create_rsa_public_keys'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'uploads',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('upload_id', sa.String(length=64), unique=True, nullable=False),  # UUID
        sa.Column('encrypted_file_data', sa.LargeBinary, nullable=False),
        sa.Column('original_filename', sa.String(length=64), nullable=True),
        sa.Column('encrypted_aes_key', sa.LargeBinary, nullable=False),  # AES key encrypted with RSA
        sa.Column('rsa_public_key_id', sa.Integer, sa.ForeignKey('rsa_public_keys.id'), nullable=False),
        sa.Column('uploaded_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
    )


def downgrade():
    op.drop_table('uploads')
