"""Add content column to posts

Revision ID: 9cab259c2feb
Revises: 49140c64df36
Create Date: 2021-11-29 22:34:36.640550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cab259c2feb'
down_revision = '49140c64df36'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
