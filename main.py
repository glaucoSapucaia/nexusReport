from matplotlib.backends.backend_pdf import PdfPages
from charts import plot_agregacao
from core import resultados_protocolos
import matplotlib.pyplot as plt
import numpy as np

# Cria o PDF
with PdfPages("relatorio_protocolos.pdf") as pdf:

    # --- Tipo ---
    plt.figure(figsize=(12, 8))
    plot_agregacao(
        resultados_protocolos["tipo"], titulo="Distribuição por Tipo", show=False
    )
    pdf.savefig()
    plt.close()

    # --- Status ---
    plt.figure(figsize=(12, 8))
    plot_agregacao(
        resultados_protocolos["status"], titulo="Distribuição por Status", show=False
    )
    pdf.savefig()
    plt.close()

    # --- Regional ---
    plt.figure(figsize=(12, 8))
    plot_agregacao(
        resultados_protocolos["regional"],
        titulo="Distribuição por Regional",
        show=False,
    )
    pdf.savefig()
    plt.close()

    # --- Grupo ---
    plt.figure(figsize=(12, 8))
    plot_agregacao(
        resultados_protocolos["grupo"], titulo="Distribuição por Grupo", show=False
    )
    pdf.savefig()
    plt.close()

    # --- Número de Vistorias ---
    # Remove NaN
    vistorias = resultados_protocolos["numero_de_vistorias"].dropna()

    plt.figure(figsize=(12, 8))
    plot_agregacao(vistorias, titulo="Distribuição por Número de Vistorias", show=False)
    pdf.savefig()
    plt.close()

    # --- Pontuação de Resolução ---
    # Remove NaN
    pontuacao = resultados_protocolos["pontuacao_resolucao"].dropna().astype(int)

    plt.figure(figsize=(12, 8))
    plot_agregacao(
        pontuacao, titulo="Distribuição por Pontuação de Resolução", show=False
    )
    pdf.savefig()
    plt.close()

    # --- Tempo de Serviço ---
    # Remove NaN e converte para int
    tempo = resultados_protocolos["tempo_servico"].dropna().astype(int)

    plt.figure(figsize=(12, 8))
    plot_agregacao(tempo, titulo="Distribuição por Tempo de Serviço", show=False)
    pdf.savefig()
    plt.close()

print("PDF gerado com sucesso: relatorio_protocolos.pdf")
