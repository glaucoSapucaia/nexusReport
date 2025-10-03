from charts.aggregration import plot_agregacao
from core import resultados_protocolos
from utils import logger

import matplotlib.pyplot as plt


def gerar_graficos_protocolos(pdf=None):
    """
    Gera gráficos de agregação para os protocolos.

    Os gráficos incluem:
        - Tipo
        - Status
        - Regional
        - Grupo
        - Número de Vistorias
        - Pontuação de Resolução
        - Tempo de Serviço
    """
    logger.info("Iniciando geração dos gráficos de protocolos.")

    try:
        # --- Tipo ---
        logger.info("Gerando gráfico: Distribuição por Tipo")
        plt.figure(figsize=(12, 8))
        plot_agregacao(
            resultados_protocolos["tipo"], titulo="Distribuição por Tipo", show=False
        )
        if pdf:
            pdf.savefig()
            logger.debug("Gráfico 'Tipo' salvo no PDF.")
        plt.close()

        # --- Status ---
        logger.info("Gerando gráfico: Distribuição por Status")
        plt.figure(figsize=(12, 8))
        plot_agregacao(
            resultados_protocolos["status"],
            titulo="Distribuição por Status",
            show=False,
        )
        if pdf:
            pdf.savefig()
            logger.debug("Gráfico 'Status' salvo no PDF.")
        plt.close()

        # --- Regional ---
        logger.info("Gerando gráfico: Distribuição por Regional")
        plt.figure(figsize=(12, 8))
        plot_agregacao(
            resultados_protocolos["regional"],
            titulo="Distribuição por Regional",
            show=False,
        )
        if pdf:
            pdf.savefig()
            logger.debug("Gráfico 'Regional' salvo no PDF.")
        plt.close()

        # --- Grupo ---
        logger.info("Gerando gráfico: Distribuição por Grupo")
        plt.figure(figsize=(12, 8))
        plot_agregacao(
            resultados_protocolos["grupo"], titulo="Distribuição por Grupo", show=False
        )
        if pdf:
            pdf.savefig()
            logger.debug("Gráfico 'Grupo' salvo no PDF.")
        plt.close()

        # --- Número de Vistorias ---
        logger.info("Gerando gráfico: Distribuição por Número de Vistorias")
        vistorias = resultados_protocolos["numero_de_vistorias"].dropna()
        plt.figure(figsize=(12, 8))
        plot_agregacao(
            vistorias, titulo="Distribuição por Número de Vistorias", show=False
        )
        if pdf:
            pdf.savefig()
            logger.debug("Gráfico 'Número de Vistorias' salvo no PDF.")
        plt.close()

        # --- Pontuação de Resolução ---
        logger.info("Gerando gráfico: Distribuição por Pontuação de Resolução")
        pontuacao = resultados_protocolos["pontuacao_resolucao"].dropna().astype(int)
        plt.figure(figsize=(12, 8))
        plot_agregacao(
            pontuacao, titulo="Distribuição por Pontuação de Resolução", show=False
        )
        if pdf:
            pdf.savefig()
            logger.debug("Gráfico 'Pontuação de Resolução' salvo no PDF.")
        plt.close()

        # --- Tempo de Serviço ---
        logger.info("Gerando gráfico: Distribuição por Tempo de Serviço")
        tempo = resultados_protocolos["tempo_servico"].dropna().astype(int)
        plt.figure(figsize=(12, 8))
        plot_agregacao(tempo, titulo="Distribuição por Tempo de Serviço", show=False)
        if pdf:
            pdf.savefig()
            logger.debug("Gráfico 'Tempo de Serviço' salvo no PDF.")
        plt.close()

        logger.info("Finalizada a geração dos gráficos de protocolos.")

    except Exception as e:
        logger.error(f"Erro ao gerar gráficos de protocolos: {e}", exc_info=True)
        raise
