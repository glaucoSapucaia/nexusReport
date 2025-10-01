from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
from .protocolo_charts import gerar_graficos_protocolos
from .rota_charts import gerar_graficos_rotas
from .visitados_charts import gerar_graficos_visitados
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams.update({"font.size": 12, "figure.titlesize": 16})


def gerar_relatorio(data_inicio):
    import locale
    from datetime import datetime

    # Define a localidade para pt_BR
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

    data_inicio = "2025-09-01"
    dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")

    mes = dt_inicio.strftime("%B")  # 'setembro'
    ano = dt_inicio.strftime("%Y")

    RELATORIO_FILENAME = f"Relatorio_GMCAT_Nexuscore_{mes}_de_{ano}.pdf"

    with PdfPages(RELATORIO_FILENAME) as pdf:
        # --- Página de título ---
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

        # --- Página de índice ---
        plt.figure(figsize=(12, 8))
        plt.axis("off")
        plt.text(0, 0.8, "Índice", fontsize=20, fontweight="bold")
        plt.text(0, 0.6, "1. Protocolos", fontsize=16)
        plt.text(0, 0.5, "2. Rotas", fontsize=16)
        plt.text(0, 0.4, "3. Vistorias", fontsize=16)
        pdf.savefig()
        plt.close()

        # --- Protocolos ---
        plt.figure(figsize=(12, 2))
        plt.axis("off")
        plt.text(0, 0.5, "1. Protocolos", fontsize=16, fontweight="bold")
        pdf.savefig()
        plt.close()
        gerar_graficos_protocolos(pdf=pdf)

        # --- Rotas ---
        plt.figure(figsize=(12, 2))
        plt.axis("off")
        plt.text(0, 0.5, "2. Rotas", fontsize=16, fontweight="bold")
        pdf.savefig()
        plt.close()
        gerar_graficos_rotas(pdf=pdf)

        # --- Vistorias ---
        plt.figure(figsize=(12, 2))
        plt.axis("off")
        plt.text(0, 0.5, "3. Vistorias", fontsize=16, fontweight="bold")
        pdf.savefig()
        plt.close()
        gerar_graficos_visitados(pdf=pdf)

        # --- Página final ---
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

    print(f"Relatório completo gerado: {RELATORIO_FILENAME}")


if __name__ == "__main__":
    gerar_relatorio()
