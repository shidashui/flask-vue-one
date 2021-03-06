"""add notifications table

Revision ID: 254bdcd8f002
Revises: e8e1580f5b43
Create Date: 2020-01-29 16:05:57.084621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '254bdcd8f002'
down_revision = 'e8e1580f5b43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_followeds_posts_read_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('last_follows_read_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('last_likes_read_time', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('last_likes_read_time')
        batch_op.drop_column('last_follows_read_time')
        batch_op.drop_column('last_followeds_posts_read_time')

    # ### end Alembic commands ###
