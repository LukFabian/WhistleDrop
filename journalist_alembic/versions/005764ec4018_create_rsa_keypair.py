"""create_rsa_keypair

Revision ID: 005764ec4018
Revises: 
Create Date: 2025-04-29 14:01:12.307481

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '005764ec4018'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'rsa_key_pairs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('public_key_pem', sa.LargeBinary, nullable=False),  # PEM-encoded public key
        sa.Column('private_key_pem', sa.LargeBinary, nullable=False),  # PEM-encoded private key
        sa.Column('is_used', sa.Boolean, default=False, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('used_at', sa.DateTime, nullable=True),
    )


def downgrade():
    op.drop_table('rsa_key_pairs')
