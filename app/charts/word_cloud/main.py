from wordcloud import WordCloud
from collections import Counter
import matplotlib
import matplotlib.pyplot as plt
from core import texto_total
from utils import stopwords_custom
from utils import logger

matplotlib.use("Agg")


def gerar_word_cloud(pdf=None):
    logger.info("Gerando nuvem de palavras para reclamações.")

    if not texto_total or texto_total.strip() == "":
        logger.warning("Texto vazio para wordcloud. Pulando geração.")
        return

    wordcloud = WordCloud(
        width=1600,
        height=800,
        background_color="white",
        stopwords=stopwords_custom,
        max_words=200,
        collocations=False,
    ).generate(texto_total)

    fig = plt.figure(figsize=(16, 9))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Nuvem de Palavras - Reclamações (Tempestivo + Intempestivo)")

    # Se estiver em relatório PDF
    if pdf:
        pdf.savefig(fig)
        plt.close(fig)
    else:
        plt.show()

    # Palavras ranqueadas
    palavras = texto_total.split()
    palavras_filtradas = [
        p for p in palavras if p not in stopwords_custom and len(p) > 2
    ]

    contagem = Counter(palavras_filtradas)
    total_palavras = sum(contagem.values())

    # Log top 30 com contagem + percentual
    top_30 = contagem.most_common(30)

    for palavra, freq in top_30:
        pct = (freq / total_palavras) * 100
        logger.info(f"{palavra:15s} | {freq:6d} | {pct:6.2f}%")
