"""create master data tables

Revision ID: 20260612_0140
Revises: 20260612_0105
Create Date: 2026-06-12 01:40:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260612_0140"
down_revision = "20260612_0105"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "permission_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_permission_categories_is_active", "permission_categories", ["is_active"], unique=False)
    op.create_index("ix_permission_categories_name", "permission_categories", ["name"], unique=True)

    op.create_table(
        "class_schedules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("course_name", sa.String(length=150), nullable=False),
        sa.Column("class_name", sa.String(length=80), nullable=False),
        sa.Column("lecturer_id", sa.Integer(), nullable=False),
        sa.Column("day", sa.String(length=20), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("room", sa.String(length=80), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["lecturer_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_class_schedules_class_name", "class_schedules", ["class_name"], unique=False)
    op.create_index("ix_class_schedules_course_name", "class_schedules", ["course_name"], unique=False)
    op.create_index("ix_class_schedules_is_active", "class_schedules", ["is_active"], unique=False)
    op.create_index("ix_class_schedules_lecturer_id", "class_schedules", ["lecturer_id"], unique=False)


def downgrade():
    op.drop_index("ix_class_schedules_lecturer_id", table_name="class_schedules")
    op.drop_index("ix_class_schedules_is_active", table_name="class_schedules")
    op.drop_index("ix_class_schedules_course_name", table_name="class_schedules")
    op.drop_index("ix_class_schedules_class_name", table_name="class_schedules")
    op.drop_table("class_schedules")

    op.drop_index("ix_permission_categories_name", table_name="permission_categories")
    op.drop_index("ix_permission_categories_is_active", table_name="permission_categories")
    op.drop_table("permission_categories")
