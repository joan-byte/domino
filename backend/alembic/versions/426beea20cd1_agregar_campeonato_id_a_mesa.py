"""Agregar campeonato_id a Mesa

Revision ID: 426beea20cd1
Revises: 4052e3087de9
Create Date: 2024-10-22 11:09:50.721752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '426beea20cd1'
down_revision: Union[str, None] = '4052e3087de9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mesas', sa.Column('partida', sa.Integer(), nullable=True))
    op.add_column('mesas', sa.Column('numero', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mesas', 'numero')
    op.drop_column('mesas', 'partida')
    # ### end Alembic commands ###
