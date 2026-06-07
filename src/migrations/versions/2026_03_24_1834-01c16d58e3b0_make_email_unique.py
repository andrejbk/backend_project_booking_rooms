"""make email unique

Revision ID: 01c16d58e3b0
Revises: 1298ae9c0e82
Create Date: 2026-03-24 18:34:33.241478

"""

from typing import Sequence, Union

from alembic import op

revision: str = "01c16d58e3b0"
down_revision: Union[str, Sequence[str], None] = "1298ae9c0e82"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")  # type: ignore
