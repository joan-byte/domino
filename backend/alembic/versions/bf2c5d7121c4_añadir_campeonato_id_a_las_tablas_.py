"""Añadir campeonato_id a las tablas jugadores y resultados

Revision ID: bf2c5d7121c4
Revises: d708c2ff2d38
Create Date: 2024-10-17 10:42:46.211299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf2c5d7121c4'
down_revision: Union[str, None] = 'd708c2ff2d38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('jugadores', sa.Column('campeonato_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'jugadores', 'campeonatos', ['campeonato_id'], ['id'])
    op.drop_constraint('mesas_campeonato_id_fkey', 'mesas', type_='foreignkey')
    op.drop_column('mesas', 'campeonato_id')
    op.add_column('resultados', sa.Column('campeonato_id', sa.Integer(), nullable=True))
    op.drop_constraint('resultados_M_fkey', 'resultados', type_='foreignkey')
    op.create_foreign_key(None, 'resultados', 'campeonatos', ['campeonato_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'resultados', type_='foreignkey')
    op.create_foreign_key('resultados_M_fkey', 'resultados', 'mesas', ['M'], ['id'])
    op.drop_column('resultados', 'campeonato_id')
    op.add_column('mesas', sa.Column('campeonato_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('mesas_campeonato_id_fkey', 'mesas', 'campeonatos', ['campeonato_id'], ['id'])
    op.drop_constraint(None, 'jugadores', type_='foreignkey')
    op.drop_column('jugadores', 'campeonato_id')
    # ### end Alembic commands ###
