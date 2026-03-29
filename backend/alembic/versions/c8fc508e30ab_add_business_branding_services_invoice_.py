"""add business branding services invoice_items

Revision ID: c8fc508e30ab
Revises:
Create Date: 2026-03-29 18:02:16.039710
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c8fc508e30ab'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _column_exists(table: str, column: str) -> bool:
    conn = op.get_bind()
    result = conn.execute(
        sa.text(
            "SELECT 1 FROM information_schema.columns "
            "WHERE table_name = :table AND column_name = :column"
        ),
        {"table": table, "column": column},
    )
    return result.fetchone() is not None


def upgrade() -> None:
    if not _column_exists("businesses", "logo_url"):
        op.add_column("businesses", sa.Column("logo_url", sa.String(500), nullable=True))
    if not _column_exists("businesses", "address"):
        op.add_column("businesses", sa.Column("address", sa.Text(), nullable=True))
    if not _column_exists("businesses", "city"):
        op.add_column("businesses", sa.Column("city", sa.String(100), nullable=True))
    if not _column_exists("businesses", "description"):
        op.add_column("businesses", sa.Column("description", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("businesses", "description")
    op.drop_column("businesses", "city")
    op.drop_column("businesses", "address")
    op.drop_column("businesses", "logo_url")
