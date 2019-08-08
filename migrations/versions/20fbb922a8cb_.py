"""empty message

Revision ID: 20fbb922a8cb
Revises: bb1e8ccc37bf
Create Date: 2018-11-09 18:40:06.169629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20fbb922a8cb'
down_revision = 'bb1e8ccc37bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('email', sa.Column('attachment', sa.String(length=250), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('email', 'attachment')
    # ### end Alembic commands ###