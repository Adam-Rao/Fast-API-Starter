"""Add foreign key to posts table

Revision ID: 7858e0b44349
Revises: 6825315f1677
Create Date: 2021-11-29 22:53:23.200706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7858e0b44349'
down_revision = '6825315f1677'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',
                          local_cols=[
                              'owner_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade():
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
