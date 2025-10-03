from charts.aggregration import (
    gerar_graficos_protocolos,
    gerar_graficos_rotas,
    gerar_graficos_vistoriados,
)
from core.analyzer import data_inicio
from utils import logger

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from datetime import datetime
import locale
from matplotlib import rcParams


rcParams.update({"font.size": 12, "figure.titlesize": 16})


def gerar_relatorio_agregacao(data_inicio=data_inicio):
    """
    Gera um relatório em PDF consolidando gráficos de protocolos, rotas e vistorias.

    O relatório contém:
        - Página de título
        - Índice
        - Seção 1: Gráficos de Protocolos
        - Seção 2: Gráficos de Rotas
        - Seção 3: Gráficos de Vistorias
        - Página final com data e hora da geração

    Args:
        data_inicio (str | datetime): Data inicial usada como referência para o relatório.
                                      Pode ser passada como string "YYYY-MM-DD" ou objeto datetime.

    Gera:
        Um arquivo PDF nomeado como:
        "Relatorio_GMCAT_Nexuscore_<mês>_de_<ano>.pdf"
    """
    logger.info("Iniciando geração do relatório consolidado.")

    try:
        # Define a localidade para pt_BR
        locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
        logger.debug("Localidade configurada para pt_BR.")

        # Normaliza data_inicio
        if isinstance(data_inicio, str):
            dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        elif isinstance(data_inicio, datetime):
            dt_inicio = data_inicio
        else:
            raise ValueError(
                "data_inicio deve ser string no formato 'YYYY-MM-DD' ou datetime."
            )

        mes = dt_inicio.strftime("%B")
        ano = dt_inicio.strftime("%Y")
        RELATORIO_FILENAME = f"Relatorio_GMCAT_Nexuscore_{mes}_de_{ano}.pdf"
        logger.info(f"Arquivo de saída definido: {RELATORIO_FILENAME}")

        with PdfPages(RELATORIO_FILENAME) as pdf:
            logger.debug("Criando página de título.")
            # Página de título
            plt.figure(figsize=(12, 8))
            plt.axis("off")
            plt.text(
                0.5,
                0.6,
                "Relatório de Dados - GMCAT Nexuscore",
                ha="center",
                va="center",
                fontsize=20,
                fontweight="bold",
            )
            plt.text(
                0.5,
                0.4,
                f"{mes} de {ano}",
                ha="center",
                va="center",
                fontsize=16,
            )
            pdf.savefig()
            plt.close()

            logger.debug("Criando página de índice.")
            # Página de índice
            plt.figure(figsize=(12, 8))
            plt.axis("off")
            plt.text(0, 0.8, "Índice", fontsize=20, fontweight="bold")
            plt.text(0, 0.6, "1. Protocolos", fontsize=16)
            plt.text(0, 0.5, "2. Rotas", fontsize=16)
            plt.text(0, 0.4, "3. Vistorias", fontsize=16)
            pdf.savefig()
            plt.close()

            # Protocolos
            logger.info("Gerando seção: Protocolos")
            plt.figure(figsize=(12, 2))
            plt.axis("off")
            plt.text(0, 0.5, "1. Protocolos", fontsize=16, fontweight="bold")
            pdf.savefig()
            plt.close()
            gerar_graficos_protocolos(pdf=pdf)

            # Rotas
            logger.info("Gerando seção: Rotas")
            plt.figure(figsize=(12, 2))
            plt.axis("off")
            plt.text(0, 0.5, "2. Rotas", fontsize=16, fontweight="bold")
            pdf.savefig()
            plt.close()
            gerar_graficos_rotas(pdf=pdf)

            # Vistorias
            logger.info("Gerando seção: Vistorias")
            plt.figure(figsize=(12, 2))
            plt.axis("off")
            plt.text(0, 0.5, "3. Vistorias", fontsize=16, fontweight="bold")
            pdf.savefig()
            plt.close()
            gerar_graficos_vistoriados(pdf=pdf)

            # Página final
            logger.debug("Criando página final com data e hora.")
            plt.figure(figsize=(12, 2))
            plt.axis("off")
            plt.text(
                0.5,
                0.5,
                f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
                ha="center",
                va="center",
                fontsize=10,
                style="italic",
            )
            pdf.savefig()
            plt.close()

        logger.info(f"Relatório gerado com sucesso: {RELATORIO_FILENAME}")

    except Exception as e:
        logger.error(f"Erro ao gerar relatório: {e}", exc_info=True)
        raise
