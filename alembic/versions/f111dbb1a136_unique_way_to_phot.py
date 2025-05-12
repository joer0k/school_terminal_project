"""unique way to phot

Revision ID: f111dbb1a136
Revises: e83cb31e66d1
Create Date: 2025-05-12 17:36:31.024415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f111dbb1a136'
down_revision: Union[str, None] = 'e83cb31e66d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
