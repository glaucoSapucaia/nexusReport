from charts.aggregration import plot_agregacao
from core import resultados_rotas
from utils import logger

import matplotlib.pyplot as plt


def gerar_graficos_rotas(pdf=None):
    """
    Gera gráficos de agregação por atributo definido.
    """
    logger.info("Iniciando geração de gráficos de rotas.")

    try:
        # --- Grupo ---
        plt.figure(figsize=(12, 8))
        logger.debug("Gerando gráfico: Distribuição por Grupo")
        plot_agregacao(
            resultados_rotas["grupo"], titulo="Distribuição por Grupo", show=False
        )
        if pdf:
            pdf.savefig()
            logger.debug("Gráfico 'Grupo' salvo no PDF.")
        plt.close()

        # --- Status ---
        plt.figure(figsize=(12, 8))
        logger.debug("Gerando gráfico: Distribuição por Status")
        plot_agregacao(
            resultados_rotas["status"],
            titulo="Distribuição por Status",
            show=False,
        )
        if pdf:
            pdf.savefig()
            logger.debug("Gráfico 'Status' salvo no PDF.")
        plt.close()

        logger.info("Finalizada a geração dos gráficos de rotas.")

    except Exception as e:
        logger.error(f"Erro ao gerar gráficos de rotas: {e}", exc_info=True)
        raise
