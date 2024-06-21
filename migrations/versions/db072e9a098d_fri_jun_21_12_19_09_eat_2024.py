"""Fri Jun 21 12:19:09 EAT 2024

Revision ID: db072e9a098d
Revises: 75e91eb501af
Create Date: 2024-06-21 12:19:09.706265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db072e9a098d'
down_revision = '75e91eb501af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('phone_number')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_number', sa.VARCHAR(length=12), nullable=True))

    # ### end Alembic commands ###