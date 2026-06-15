"""create users table

Revision ID: 20260612_0105
Revises:
Create Date: 2026-06-12 01:05:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260612_0105"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "role",
            sa.Enum("mahasiswa", "dosen", "admin", name="user_role"),
            nullable=False,
        ),
        sa.Column("student_number", sa.String(length=40), nullable=True),
        sa.Column("lecturer_code", sa.String(length=40), nullable=True),
        sa.Column("phone", sa.String(length=30), nullable=True),
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
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_is_active", "users", ["is_active"], unique=False)
    op.create_index("ix_users_lecturer_code", "users", ["lecturer_code"], unique=True)
    op.create_index("ix_users_role", "users", ["role"], unique=False)
    op.create_index("ix_users_student_number", "users", ["student_number"], unique=True)


def downgrade():
    op.drop_index("ix_users_student_number", table_name="users")
    op.drop_index("ix_users_role", table_name="users")
    op.drop_index("ix_users_lecturer_code", table_name="users")
    op.drop_index("ix_users_is_active", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
