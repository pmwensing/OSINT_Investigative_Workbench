from alembic import op
import sqlalchemy as sa


revision = "0002_jobs_target_nullable"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("jobs", "target_id", existing_type=sa.UUID(), nullable=True)


def downgrade() -> None:
    op.alter_column("jobs", "target_id", existing_type=sa.UUID(), nullable=False)
