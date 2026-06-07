"""add users

Revision ID: 1298ae9c0e82
Revises: 803d01893858
Create Date: 2026-03-22 08:51:29.928427

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "1298ae9c0e82"
down_revision: Union[str, Sequence[str], None] = "803d01893858"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
