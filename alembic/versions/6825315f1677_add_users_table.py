"""Add users table

Revision ID: 6825315f1677
Revises: 9cab259c2feb
Create Date: 2021-11-29 22:43:36.194351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6825315f1677'
down_revision = '9cab259c2feb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('users')
