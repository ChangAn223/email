"""empty message

Revision ID: ca26c581e324
Revises: 20fbb922a8cb
Create Date: 2018-11-09 20:02:06.344965

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ca26c581e324'
down_revision = '20fbb922a8cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'passwd',
               existing_type=mysql.VARCHAR(length=100),
               type_=sa.String(length=150),
               existing_nullable=True)
    op.alter_column('user', 'sign',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=60),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'sign',
               existing_type=sa.String(length=60),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)
    op.alter_column('user', 'passwd',
               existing_type=sa.String(length=150),
               type_=mysql.VARCHAR(length=100),
               existing_nullable=True)
    # ### end Alembic commands ###
