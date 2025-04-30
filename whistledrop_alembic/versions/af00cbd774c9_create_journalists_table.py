"""create journalists table

Revision ID: af00cbd774c9
Revises: 0002_create_uploads
Create Date: 2025-04-29 19:15:27.264104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af00cbd774c9'
down_revision: Union[str, None] = '0002_create_uploads'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'journalists',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(length=50), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(length=128), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('journalists')
