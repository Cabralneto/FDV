"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-03-06
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("obras", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("nome", sa.String(length=255), nullable=False, unique=True))


def downgrade() -> None:
    op.drop_table("obras")
