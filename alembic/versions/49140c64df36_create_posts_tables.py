"""Create posts tables

Revision ID: 49140c64df36
Revises: 
Create Date: 2021-11-29 22:26:05.984320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49140c64df36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer, nullable=False,
                    primary_key=True), sa.Column('title', sa.String, nullable=False))


def downgrade():
    op.drop_table('posts')
