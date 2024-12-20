"""empty message

Revision ID: 7fc0dfae9d8a
Revises: 263aff30a40d
Create Date: 2024-08-21 13:31:10.763170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7fc0dfae9d8a'
down_revision: Union[str, None] = '263aff30a40d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('balances', 'currency')
    op.add_column('payments', sa.Column('date_time', sa.DateTime(), nullable=True))
    op.add_column('payments_sites', sa.Column('hash_rate', sa.BigInteger(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payments_sites', 'hash_rate')
    op.drop_column('payments', 'date_time')
    op.add_column('balances', sa.Column('currency', sa.VARCHAR(length=8), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
