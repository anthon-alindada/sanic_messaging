"""create message table

Revision ID: 39321e8679f1
Revises: 6aaa4944119c
Create Date: 2019-03-22 19:02:36.887561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39321e8679f1'
down_revision = '6aaa4944119c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('content', sa.Text),
        sa.Column('author_id', sa.Integer),
        sa.Column('channel_id', sa.Integer),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('edited_timestamp', sa.DateTime, nullable=False),
    )
    op.create_foreign_key(
        None, 'messages', 'users',
        ['author_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(
        None, 'messages', 'channels',
        ['channel_id'], ['id'], ondelete='CASCADE')


def downgrade():
    op.drop_table('messages')
