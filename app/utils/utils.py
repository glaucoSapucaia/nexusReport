import re
import unidecode
import pandas as pd
from wordcloud import STOPWORDS


def limpar_texto(texto):
    if pd.isna(texto):
        return ""

    texto = texto.lower()
    texto = unidecode.unidecode(texto)  # remove acentos
    texto = re.sub(r"\d+", "", texto)  # remove números
    texto = re.sub(r"[^\w\s]", " ", texto)  # remove pontuação
    texto = re.sub(r"\s+", " ", texto)  # espaços extras

    # Anonimização
    texto = re.sub(r"\b\d{11}\b", "", texto)  # CPF
    texto = re.sub(r"\b\d{6,}\b", "", texto)  # inscrições longas
    return texto.strip()


# Word Cloud
stopwords_custom = set(STOPWORDS)
stopwords_custom.update(
    [
        "de",
        "da",
        "do",
        "das",
        "dos",
        "e",
        "a",
        "o",
        "que",
        "para",
        "por",
        "em",
        "com",
        "nao",
        "sim",
        "ou",
        "como",
        "qualquer",
    ]
)
