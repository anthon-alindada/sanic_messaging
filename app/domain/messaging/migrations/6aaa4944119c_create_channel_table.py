"""create channel table

Revision ID: 6aaa4944119c
Revises:
Create Date: 2019-03-02 13:08:23.327765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6aaa4944119c'
down_revision = None
branch_labels = ('messaging',)
depends_on = None


def upgrade():
    op.create_table(
        'channels',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('is_channel', sa.Boolean, default=True),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('edited_timestamp', sa.DateTime, nullable=False),
    )
    op.create_foreign_key(
        None, 'channels', 'users',
        ['owner_id'], ['id'], ondelete='CASCADE')


def downgrade():
    op.drop_table('channels')
