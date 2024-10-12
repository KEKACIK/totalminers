"""empty message

Revision ID: 8a8f52ea6977
Revises: 5fa38ee4ac90
Create Date: 2024-08-13 09:05:25.960360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a8f52ea6977'
down_revision: Union[str, None] = '5fa38ee4ac90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('value', sa.BigInteger(), nullable=True),
    sa.Column('current_balance', sa.BigInteger(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments_sites',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('site_id', sa.String(), nullable=True),
    sa.Column('payment_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['payment_id'], ['payments.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments_sites')
    op.drop_table('payments')
    # ### end Alembic commands ###
