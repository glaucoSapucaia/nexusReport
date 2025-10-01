from charts import plot_agregacao
from core import resultados_pontos_visitados
import matplotlib.pyplot as plt


# Cria o PDF
def gerar_graficos_visitados(pdf: None):
    # --- Grupo---
    plt.figure(figsize=(12, 8))
    plot_agregacao(
        resultados_pontos_visitados["resultado"],
        titulo="Distribuição por Resultado",
        show=False,
    )
    if pdf:
        pdf.savefig()
    plt.close()

    # --- Status ---
    plt.figure(figsize=(12, 8))
    plot_agregacao(
        resultados_pontos_visitados["responsavel"],
        titulo="Distribuição por Responsavel",
        show=False,
    )
    if pdf:
        pdf.savefig()
    plt.close()

    print("PDF gerado com sucesso: graficos_pontos_vistoriados.pdf")
