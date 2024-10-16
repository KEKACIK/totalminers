"""empty message

Revision ID: e498dc2a1731
Revises: a9dec00bed22
Create Date: 2024-08-16 14:29:05.185014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e498dc2a1731'
down_revision: Union[str, None] = 'a9dec00bed22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('buy_request_miner_items', sa.Column('created', sa.DateTime(), nullable=True))
    op.add_column('buy_requests', sa.Column('created', sa.DateTime(), nullable=True))
    op.add_column('miner_items', sa.Column('created', sa.DateTime(), nullable=True))
    op.add_column('payments_sites', sa.Column('created', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payments_sites', 'created')
    op.drop_column('miner_items', 'created')
    op.drop_column('buy_requests', 'created')
    op.drop_column('buy_request_miner_items', 'created')
    # ### end Alembic commands ###
