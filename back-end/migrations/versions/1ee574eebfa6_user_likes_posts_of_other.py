"""user likes posts of other

Revision ID: 1ee574eebfa6
Revises: 15343434f098
Create Date: 2020-02-06 16:18:09.319259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ee574eebfa6'
down_revision = '15343434f098'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts_likes',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], name=op.f('fk_posts_likes_post_id_posts')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_posts_likes_user_id_users'))
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_comments_likes_read_time', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('last_posts_likes_read_time', sa.DateTime(), nullable=True))
        batch_op.drop_column('last_likes_read_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_likes_read_time', sa.DATETIME(), nullable=True))
        batch_op.drop_column('last_posts_likes_read_time')
        batch_op.drop_column('last_comments_likes_read_time')

    op.drop_table('posts_likes')
    # ### end Alembic commands ###