"""update User -> username nullable=False

Revision ID: 99e29b5ed74f
Revises: 8db6000bc97c
Create Date: 2025-03-31 04:04:57.330048

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "99e29b5ed74f"
down_revision: Union[str, None] = "8db6000bc97c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "userprofile",
        "username",
        existing_type=sa.VARCHAR(length=50),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "userprofile",
        "username",
        existing_type=sa.VARCHAR(length=50),
        nullable=True,
    )
    # ### end Alembic commands ###
