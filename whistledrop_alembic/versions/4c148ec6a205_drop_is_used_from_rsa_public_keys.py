"""Drop is_used from rsa_public_keys

Revision ID: 4c148ec6a205
Revises: af00cbd774c9
Create Date: 2025-04-30 12:14:26.323562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c148ec6a205'
down_revision: Union[str, None] = 'af00cbd774c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    from alembic import op
    op.drop_column('rsa_public_keys', 'is_used')
    op.drop_column('rsa_public_keys', 'created_at')
    op.drop_column('rsa_public_keys', 'used_at')


def downgrade():
    from alembic import op
    import sqlalchemy as sa
    op.add_column('rsa_public_keys', sa.Column('is_used', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('rsa_public_keys', sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False))
    op.add_column('rsa_public_keys', sa.Column('used_at', sa.DateTime, nullable=True))
