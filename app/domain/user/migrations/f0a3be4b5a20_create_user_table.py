"""create user table

Revision ID: f0a3be4b5a20
Revises:
Create Date: 2019-03-01 21:53:50.537581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0a3be4b5a20'
down_revision = None
branch_labels = ('user',)
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('active', sa.Boolean, default=False),
        sa.Column('date_joined', sa.DateTime, nullable=False),
        sa.Column('password', sa.String(128)),
    )


def downgrade():
    op.drop_table('users')
