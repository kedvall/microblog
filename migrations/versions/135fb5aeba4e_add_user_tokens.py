"""Add user tokens

Revision ID: 135fb5aeba4e
Revises: 4da107a5d439
Create Date: 2020-11-04 22:37:33.608520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '135fb5aeba4e'
down_revision = '4da107a5d439'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('token', sa.String(length=32), nullable=True))
    op.add_column('user', sa.Column('token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_column('user', 'token_expiration')
    op.drop_column('user', 'token')
    # ### end Alembic commands ###