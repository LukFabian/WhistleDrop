"""create rsa_public_keys table

Revision ID: fd60fcf061b5
Revises: 
Create Date: 2025-04-25 14:12:16.886068

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers
revision = '0001_create_rsa_public_keys'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'rsa_public_keys',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('public_key_pem', sa.LargeBinary, nullable=False),  # PEM-encoded public key
        sa.Column('is_used', sa.Boolean, default=False, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('used_at', sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table('rsa_public_keys')
