"""Actualizar restricción única de jugador

Revision ID: cf7c3a23ebc0
Revises: 671d7c31b184
Create Date: 2024-10-23 13:45:47.565128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf7c3a23ebc0'
down_revision: Union[str, None] = '671d7c31b184'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_jugador', 'jugadores', type_='unique')
    op.create_unique_constraint('uq_jugador_campeonato', 'jugadores', ['nombre', 'apellido', 'campeonato_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_jugador_campeonato', 'jugadores', type_='unique')
    op.create_unique_constraint('uq_jugador', 'jugadores', ['nombre', 'apellido'])
    # ### end Alembic commands ###
