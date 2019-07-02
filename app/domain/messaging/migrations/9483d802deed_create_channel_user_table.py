"""create channel user table

Revision ID: 9483d802deed
Revises: 39321e8679f1
Create Date: 2019-06-11 08:06:28.011755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9483d802deed'
down_revision = '39321e8679f1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'channel_users',
        sa.Column('user_id', sa.Integer),
        sa.Column('channel_id', sa.Integer),
    )
    op.create_foreign_key(
        None, 'channel_users', 'users',
        ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(
        None, 'channel_users', 'channels',
        ['channel_id'], ['id'], ondelete='CASCADE')


def downgrade():
    op.drop_table('channel_users')
