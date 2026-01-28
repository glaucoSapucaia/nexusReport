from .protocolos import resultados as resultados_protocolos
from .protocolos import (
    resultados_grupo_tempo_servico,
    resultados_tempestivo_intempestivo,
    resultado_reclamacao,
    texto_total,
)
from .rotas import resultados as resultados_rotas
from .pontos_visitados import resultados as resultados_pontos_visitados
from .insights import resultados_insights

__all__ = [
    "resultados_protocolos",
    "resultados_grupo_tempo_servico",
    "resultados_rotas",
    "resultados_pontos_visitados",
    "resultados_insights",
    "resultados_tempestivo_intempestivo",
    "resultado_reclamacao",
    "texto_total",
]
