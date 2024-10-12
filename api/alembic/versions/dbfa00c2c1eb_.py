"""empty message

Revision ID: dbfa00c2c1eb
Revises: e498dc2a1731
Create Date: 2024-08-16 15:25:58.000915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbfa00c2c1eb'
down_revision: Union[str, None] = 'e498dc2a1731'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('billings', sa.Column('payment_type', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('billings', 'payment_type')
    # ### end Alembic commands ###