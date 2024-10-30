"""renombrar_columnas_ranking_final

Revision ID: 10b05350d6c1
Revises: 
Create Date: 2024-10-30 11:53:52.841380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10b05350d6c1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rankings_finales', sa.Column('PG', sa.Integer(), nullable=True))
    op.add_column('rankings_finales', sa.Column('PP', sa.Integer(), nullable=True))
    op.drop_column('rankings_finales', 'puntos_perdidos')
    op.drop_column('rankings_finales', 'puntos_ganados')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rankings_finales', sa.Column('puntos_ganados', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('rankings_finales', sa.Column('puntos_perdidos', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('rankings_finales', 'PP')
    op.drop_column('rankings_finales', 'PG')
    # ### end Alembic commands ###
