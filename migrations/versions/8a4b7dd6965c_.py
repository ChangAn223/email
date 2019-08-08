"""empty message

Revision ID: 8a4b7dd6965c
Revises: 23b33df95cd6
Create Date: 2018-11-09 18:39:15.433019

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8a4b7dd6965c'
down_revision = '23b33df95cd6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('draft')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('draft',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('send_man', mysql.VARCHAR(length=40), nullable=True),
    sa.Column('theme', mysql.VARCHAR(length=200), nullable=False),
    sa.Column('content', mysql.TEXT(), nullable=True),
    sa.Column('attachment', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('add_time', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###