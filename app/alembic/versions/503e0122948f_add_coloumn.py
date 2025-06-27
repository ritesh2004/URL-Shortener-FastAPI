"""add coloumn

Revision ID: 503e0122948f
Revises: f2a9cfd85fdc
Create Date: 2025-06-28 00:15:45.242988

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '503e0122948f'
down_revision: Union[str, Sequence[str], None] = 'f2a9cfd85fdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('url', sa.Column('expiration_time', sa.String(length=255), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
