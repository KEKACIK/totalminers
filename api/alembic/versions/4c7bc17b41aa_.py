"""empty message

Revision ID: 4c7bc17b41aa
Revises: f27c7c39aef8
Create Date: 2024-08-10 10:40:28.357781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c7bc17b41aa'
down_revision: Union[str, None] = 'f27c7c39aef8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('miner_items', 'buy_cost')
    op.drop_column('miner_items', 'hashrate')
    op.drop_column('miner_items', 'dohod')
    op.drop_column('miner_items', 'profit')
    op.drop_column('miner_items', 'hosting_cost')
    op.drop_column('miner_items', 'rashod')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('miner_items', sa.Column('rashod', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('miner_items', sa.Column('hosting_cost', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('miner_items', sa.Column('profit', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('miner_items', sa.Column('dohod', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('miner_items', sa.Column('hashrate', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('miner_items', sa.Column('buy_cost', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
