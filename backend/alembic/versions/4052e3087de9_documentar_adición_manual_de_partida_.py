"""Documentar adición manual de partida_actual a Campeonato

Revision ID: 4052e3087de9
Revises: 00de75fa6e76
Create Date: 2024-10-22 10:19:17.739740

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4052e3087de9'
down_revision: Union[str, None] = '00de75fa6e76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
