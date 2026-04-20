from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def run_uuid_default(column_name: str) -> sa.TextClause:
    return sa.text("gen_random_uuid()")

def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "investigations",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("owner_user_id", sa.UUID(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "targets",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("investigation_id", sa.UUID(), sa.ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("target_type", sa.String(length=50), nullable=False),
        sa.Column("value", sa.String(length=512), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "jobs",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("investigation_id", sa.UUID(), sa.ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("target_id", sa.UUID(), sa.ForeignKey("targets.id", ondelete="CASCADE"), nullable=False),
        sa.Column("connector", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="queued"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("queued_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "artifacts",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("investigation_id", sa.UUID(), sa.ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", sa.UUID(), sa.ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("artifact_type", sa.String(length=100), nullable=False),
        sa.Column("bucket", sa.String(length=128), nullable=False),
        sa.Column("object_key", sa.String(length=1024), nullable=False),
        sa.Column("content_type", sa.String(length=128), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "entities",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("investigation_id", sa.UUID(), sa.ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("source_job_id", sa.UUID(), sa.ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "observables",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("investigation_id", sa.UUID(), sa.ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("observable_type", sa.String(length=50), nullable=False),
        sa.Column("value", sa.String(length=1024), nullable=False),
        sa.Column("normalized_value", sa.String(length=1024), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("source_job_id", sa.UUID(), sa.ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_observables_lookup", "observables", ["investigation_id", "observable_type", "normalized_value"])

    op.create_table(
        "relationships",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("investigation_id", sa.UUID(), sa.ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("source_entity_id", sa.UUID(), sa.ForeignKey("entities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("target_entity_id", sa.UUID(), sa.ForeignKey("entities.id", ondelete="CASCADE"), nullable=False),
        sa.Column("relationship_type", sa.String(length=100), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("source_job_id", sa.UUID(), sa.ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "entity_observables",
        sa.Column("entity_id", sa.UUID(), sa.ForeignKey("entities.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("observable_id", sa.UUID(), sa.ForeignKey("observables.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "claims",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("investigation_id", sa.UUID(), sa.ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", sa.UUID(), sa.ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("claim_type", sa.String(length=100), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "contradictions",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("investigation_id", sa.UUID(), sa.ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("left_claim_id", sa.UUID(), sa.ForeignKey("claims.id", ondelete="CASCADE"), nullable=False),
        sa.Column("right_claim_id", sa.UUID(), sa.ForeignKey("claims.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False, server_default="0.5"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "timeline_events",
        sa.Column("id", sa.UUID(), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("investigation_id", sa.UUID(), sa.ForeignKey("investigations.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_id", sa.UUID(), sa.ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True),
        sa.Column("event_time", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

def downgrade() -> None:
    op.drop_table("timeline_events")
    op.drop_table("contradictions")
    op.drop_table("claims")
    op.drop_table("entity_observables")
    op.drop_table("relationships")
    op.drop_index("ix_observables_lookup", table_name="observables")
    op.drop_table("observables")
    op.drop_table("entities")
    op.drop_table("artifacts")
    op.drop_table("jobs")
    op.drop_table("targets")
    op.drop_table("investigations")
    op.drop_table("users")
