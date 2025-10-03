from charts.aggregration import plot_agregacao
from core import resultados_pontos_visitados
from utils import logger

import matplotlib.pyplot as plt


def gerar_graficos_vistoriados(pdf=None):
    """
    Gera gráficos de agregação por atributo definido.
    """
    logger.info("Iniciando geração de gráficos de vistoria.")

    try:
        # --- Resultado ---
        plt.figure(figsize=(12, 8))
        logger.debug("Gerando gráfico: Distribuição por Resultado")
        plot_agregacao(
            resultados_pontos_visitados["resultado"],
            titulo="Distribuição por Resultado",
            show=False,
        )
        if pdf:
            pdf.savefig()
            logger.debug("Gráfico 'Resultado' salvo no PDF.")
        plt.close()

        # --- Responsável ---
        plt.figure(figsize=(12, 8))
        logger.debug("Gerando gráfico: Distribuição por Responsável")
        plot_agregacao(
            resultados_pontos_visitados["responsavel"],
            titulo="Distribuição por Responsavel",
            show=False,
        )
        if pdf:
            pdf.savefig()
            logger.debug("Gráfico 'Responsável' salvo no PDF.")
        plt.close()

        logger.info("Finalizada a geração dos gráficos de vistoria.")

    except Exception as e:
        logger.error(f"Erro ao gerar gráficos de vistoria: {e}", exc_info=True)
        raise
