from utils import logger

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np


def plot_agregacao(
    serie, titulo=None, tipo="bar", show=True, horizontal=True, rotacao_x=45
):
    """
    Gera gráfico a partir de uma Series (value_counts)

    Parameters:
    - serie: pd.Series (resultado do value_counts)
    - titulo: str, título do gráfico
    - tipo: 'bar' ou 'pie'
    - show: bool, se True exibe o gráfico, se False só desenha (útil para salvar PDF)
    - horizontal: bool, se True usa barras horizontais (barh), ideal para muitas categorias
    - rotacao_x: rotação dos labels (só usada se horizontal=False)
    """
    try:
        logger.info(
            f"Iniciando plotagem: '{titulo or 'Agregação'}', tipo='{tipo}', categorias={len(serie)}"
        )

        plt.figure(figsize=(12, 8))

        # Ordena série para gráfico mais legível
        dados = serie.sort_values()

        if tipo == "bar":
            if horizontal:
                cores = cm.tab20(np.linspace(0, 1, len(dados)))
                ax = dados.plot(kind="barh", color=cores)
                plt.xlabel("Contagem")
                plt.ylabel("")

                for i, v in enumerate(dados):
                    if v / max(dados) > 0.8:
                        ax.text(
                            v - max(dados) * 0.02,
                            i,
                            str(v),
                            color="black",
                            va="center",
                            ha="right",
                        )
                    else:
                        ax.text(
                            v + max(dados) * 0.01, i, str(v), color="black", va="center"
                        )
            else:
                cores = cm.tab20(np.linspace(0, 1, len(dados)))
                ax = dados.plot(kind="bar", color=cores)
                plt.ylabel("Contagem")
                plt.xlabel("")
                plt.xticks(rotation=rotacao_x)

                for i, v in enumerate(dados):
                    ax.text(i, v + 1, str(v), color="black", ha="center")

        elif tipo == "pie":
            dados.plot(kind="pie", autopct="%1.1f%%")
            plt.ylabel("")

        plt.title(titulo or "Agregação")
        plt.tight_layout()

        if show:
            plt.show()

        logger.info(f"Plotagem concluída: '{titulo or 'Agregação'}'")

    except Exception as e:
        logger.error(
            f"Erro ao gerar gráfico '{titulo or 'Agregação'}': {e}", exc_info=True
        )
        raise
