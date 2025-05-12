"""столбец posts

Revision ID: e83cb31e66d1
Revises: 40153099f88f
Create Date: 2025-05-12 17:29:25.181756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e83cb31e66d1'
down_revision: Union[str, None] = '40153099f88f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
