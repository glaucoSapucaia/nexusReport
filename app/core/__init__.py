from .protocolos import resultados as resultados_protocolos
from .protocolos import resultados_grupo_tempo_servico
from .protocolos import resultados_tempestivo_intempestivo
from .protocolos import resultado_reclamacao
from .rotas import resultados as resultados_rotas
from .pontos_visitados import resultados as resultados_pontos_visitados

__all__ = [
    "resultados_protocolos",
    "resultados_grupo_tempo_servico",
    "resultados_rotas",
    "resultados_pontos_visitados",
    "resultados_tempestivo_intempestivo",
    "resultado_reclamacao",
]
