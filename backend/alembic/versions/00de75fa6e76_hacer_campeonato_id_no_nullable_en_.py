"""Hacer campeonato_id no nullable en jugadores y resultados

Revision ID: 00de75fa6e76
Revises: bf2c5d7121c4
Create Date: 2024-10-17 10:50:37.740309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00de75fa6e76'
down_revision: Union[str, None] = 'bf2c5d7121c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
