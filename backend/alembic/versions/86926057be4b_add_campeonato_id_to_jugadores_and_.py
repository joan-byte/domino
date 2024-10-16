"""add_campeonato_id_to_jugadores_and_resultados

Revision ID: 86926057be4b
Revises: aa9324bf1f0c
Create Date: 2024-10-16 12:30:37.519147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86926057be4b'
down_revision: Union[str, None] = 'aa9324bf1f0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
