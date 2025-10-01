from matplotlib.backends.backend_pdf import PdfPages
from charts import plot_agregacao
from core import resultados_rotas
import matplotlib.pyplot as plt


# Cria o PDF
def gerar_graficos_rotas(pdf=None):
    # --- Grupo---
    plt.figure(figsize=(12, 8))
    plot_agregacao(
        resultados_rotas["grupo"], titulo="Distribuição por Grupo", show=False
    )
    if pdf:
        pdf.savefig()
    plt.close()

    # --- Status ---
    plt.figure(figsize=(12, 8))
    plot_agregacao(
        resultados_rotas["status"],
        titulo="Distribuição por Status",
        show=False,
    )
    if pdf:
        pdf.savefig()
    plt.close()

    print("PDF gerado com sucesso: graficos_rotas.pdf")
