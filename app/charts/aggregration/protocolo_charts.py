import re
from charts.aggregration import plot_agregacao
from core import (
    resultados_protocolos,
    resultados_grupo_tempo_servico,
    resultados_tempestivo_intempestivo,
    resultado_reclamacao,
)
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
        plt.close()

        # --- Tipo Tempestivo/Intempestivo ---
        logger.info("Gerando gráfico: Distribuição por Tempestividade")
        plt.figure(figsize=(12, 8))
        plot_agregacao(
            resultados_tempestivo_intempestivo["tipo"],
            titulo="Distribuição por Tempestividade",
            show=False,
        )
        if pdf:
            pdf.savefig()
        plt.close()

        # --- Reclamação ---
        logger.info("Gerando gráfico: Distribuição por Reclamação")
        plt.figure(figsize=(12, 8))
        plot_agregacao(
            resultado_reclamacao,
            titulo="Distribuição por Reclamação",
            show=False,
        )
        if pdf:
            pdf.savefig()
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
        plt.close()

        # --- Grupo ---
        logger.info("Gerando gráfico: Distribuição por Grupo")
        plt.figure(figsize=(12, 8))
        plot_agregacao(
            resultados_protocolos["grupo"], titulo="Distribuição por Grupo", show=False
        )
        if pdf:
            pdf.savefig()
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
        plt.close()

        # --- Tempo de Serviço ---
        logger.info("Gerando gráfico: Distribuição por Tempo de Serviço")
        tempo = resultados_protocolos["tempo_servico"].dropna().astype(int)
        plt.figure(figsize=(12, 8))
        plot_agregacao(tempo, titulo="Distribuição por Tempo de Serviço", show=False)
        if pdf:
            pdf.savefig()
        plt.close()

        # --- Tempo de Serviço por Grupo ---
        logger.info("Gerando gráfico: Tempo de Serviço Total por Grupo")
        plt.figure(figsize=(12, 8))

        # resultados_grupo_tempo_servico deve ser um pd.Series ou dict com {grupo: tempo_total}
        plot_agregacao(
            resultados_grupo_tempo_servico,
            titulo="Tempo de Serviço Total por Grupo",
            show=False,
        )
        if pdf:
            pdf.savefig()
        plt.close()

        logger.info("Finalizada a geração dos gráficos de protocolos.")

    except Exception as e:
        logger.error(f"Erro ao gerar gráficos de protocolos: {e}", exc_info=True)
        raise
