# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.jugador import Jugador, Pareja  # noqa
from app.models.campeonato import Campeonato  # noqa
from app.models.mesa import Mesa  # noqa
from app.models.resultado import Resultado  # noqa
# Importe aquí otros modelos si los tiene
