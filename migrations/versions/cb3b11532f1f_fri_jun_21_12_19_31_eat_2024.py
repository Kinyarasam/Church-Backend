"""Fri Jun 21 12:19:31 EAT 2024

Revision ID: cb3b11532f1f
Revises: db072e9a098d
Create Date: 2024-06-21 12:19:31.861300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb3b11532f1f'
down_revision = 'db072e9a098d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('phone_number', sa.String(length=12), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('phone_number')

    # ### end Alembic commands ###
