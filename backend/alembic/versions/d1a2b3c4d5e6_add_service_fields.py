"""add service billing fields

Revision ID: d1a2b3c4d5e6
Revises: c8fc508e30ab
Create Date: 2026-03-29 21:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'd1a2b3c4d5e6'
down_revision: Union[str, None] = 'c8fc508e30ab'
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
    if not _column_exists("services", "category"):
        op.add_column("services", sa.Column("category", sa.String(100), nullable=True))
    if not _column_exists("services", "billing_type"):
        op.add_column("services", sa.Column("billing_type", sa.String(20), nullable=True, server_default="one_time"))
    if not _column_exists("services", "billing_cycle"):
        op.add_column("services", sa.Column("billing_cycle", sa.String(20), nullable=True))
    if not _column_exists("services", "unit"):
        op.add_column("services", sa.Column("unit", sa.String(50), nullable=True))


def downgrade() -> None:
    op.drop_column("services", "unit")
    op.drop_column("services", "billing_cycle")
    op.drop_column("services", "billing_type")
    op.drop_column("services", "category")
