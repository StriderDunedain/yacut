"""Perhaps migrations will help

Revision ID: 4497c0d62379
Revises: 
Create Date: 2024-01-07 00:13:06.118483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4497c0d62379'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db.sqlite3', sa.Column('test_field', sa.String(length=1), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('db.sqlite3', 'test_field')
    # ### end Alembic commands ###
