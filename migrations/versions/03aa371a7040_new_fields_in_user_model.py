"""New fields in user model

Revision ID: 03aa371a7040
Revises: 2c382381a17b
Create Date: 2018-07-10 13:51:43.894894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03aa371a7040'
down_revision = '2c382381a17b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
