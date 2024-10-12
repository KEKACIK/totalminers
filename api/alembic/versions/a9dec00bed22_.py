"""empty message

Revision ID: a9dec00bed22
Revises: 75f3a8e0b23d
Create Date: 2024-08-16 14:21:27.494287

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9dec00bed22'
down_revision: Union[str, None] = '75f3a8e0b23d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('buy_request_miner_items', sa.Column('count', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('created', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'created')
    op.drop_column('buy_request_miner_items', 'count')
    # ### end Alembic commands ###