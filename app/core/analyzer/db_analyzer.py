import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from utils import logger
from pathlib import Path

ENV_DIR = Path(__file__).resolve().parent.parent.parent.parent / ".env"

data_inicio = "2026-04-01"
data_fim = "2026-04-30"


class DBAnalyzer:
    def __init__(self, env_path=ENV_DIR):
        logger.info("Inicializando DBAnalyzer...")
        load_dotenv(env_path)

        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")
        self.data_inicio = data_inicio
        self.data_fim = data_fim

        try:
            # Cria a engine SQLAlchemy
            self.engine = create_engine(
                f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
            )
            self.inspector = inspect(self.engine)
            self.dfs = {}
            logger.info(
                f"Conexão estabelecida com o banco: {self.db_name}@{self.db_host}"
            )
        except Exception as e:
            logger.error(f"Erro ao conectar no banco de dados: {e}", exc_info=True)
            raise

    def carregar_tabelas(self, tabelas):
        """Carrega tabelas do banco para DataFrames"""
        for tabela in tabelas:
            try:
                if tabela in self.inspector.get_table_names(schema="public"):
                    self.dfs[tabela] = pd.read_sql_table(
                        tabela, self.engine, schema="public"
                    )
                else:
                    logger.warning(f"Tabela '{tabela}' não encontrada no banco")
            except Exception as e:
                logger.error(f"Erro ao carregar tabela {tabela}: {e}", exc_info=True)
                raise
        return self.dfs

    def filtrar_periodo(self, tabela, coluna_data):
        """
        Filtra registros de uma tabela entre uma data inicial e final.
        """
        df = self.dfs.get(tabela)
        if df is None:
            logger.error(f"Tabela '{tabela}' não carregada.")
            raise ValueError(f"Tabela {tabela} não carregada.")

        # Converte para datetime e remove timezone
        df[coluna_data] = pd.to_datetime(df[coluna_data]).dt.tz_localize(None)

        # Converte parâmetros para datetime se forem strings
        if self.data_inicio is not None and isinstance(self.data_inicio, str):
            self.data_inicio = pd.to_datetime(self.data_inicio)
        if self.data_fim is not None and isinstance(self.data_fim, str):
            self.data_fim = pd.to_datetime(self.data_fim)

        # Filtra conforme datas
        if self.data_inicio is not None:
            df = df[df[coluna_data] >= self.data_inicio]
        if self.data_fim is not None:
            df = df[df[coluna_data] <= self.data_fim]

        return df

    def agregacoes(self, df, colunas, top_n=None):
        """
        Realiza agregações simples (value_counts) para várias colunas,
        remove NaN e converte valores para int.
        """
        resultados = {}

        for coluna in colunas:
            try:
                # Normaliza textos se forem strings
                if pd.api.types.is_string_dtype(df[coluna]):
                    df[coluna] = df[coluna].str.title().str.strip()

                # Conta ocorrências
                vc = df[coluna].value_counts(dropna=True)

                # Se top_n definido, agrupa o resto em "Outros"
                if top_n is not None and len(vc) > top_n:
                    top = vc.iloc[:top_n]
                    outros = vc.iloc[top_n:].sum()
                    vc = top.append(pd.Series({"Outros": outros}))

                # Converte index numérico para int quando possível
                if pd.api.types.is_float_dtype(vc.index):
                    vc.index = vc.index.astype(int)

                resultados[coluna] = vc

            except Exception as e:
                logger.error(f"Erro ao agregar coluna {coluna}: {e}", exc_info=True)
                raise
        return resultados

    def agregacao_soma_por_grupo(self, df, coluna_agregar, coluna_somar):
        """
        Agrega dados por uma coluna e soma os valores de outra coluna, retornando inteiros.

        Parâmetros:
            df (pd.DataFrame): DataFrame com os dados.
            coluna_agregar (str): Coluna que será usada para agrupar (ex: 'grupo').
            coluna_somar (str): Coluna que será somada (ex: 'tempo_servico').

        Retorna:
            pd.Series: Série com a soma do tempo de serviço por grupo (tipo int).
        """

        if coluna_agregar not in df.columns or coluna_somar not in df.columns:
            logger.error(
                f"Colunas '{coluna_agregar}' ou '{coluna_somar}' não encontradas no DataFrame"
            )
            raise ValueError(
                f"Colunas '{coluna_agregar}' ou '{coluna_somar}' não encontradas no DataFrame"
            )

        try:
            # Normaliza coluna de agrupamento se for string
            if pd.api.types.is_string_dtype(df[coluna_agregar]):
                df[coluna_agregar] = df[coluna_agregar].str.title().str.strip()

            # Garante que a coluna a somar seja numérica, substituindo NaNs por 0
            df[coluna_somar] = pd.to_numeric(df[coluna_somar], errors="coerce").fillna(
                0
            )

            # Agrupa e soma
            resultados = (
                df.groupby(coluna_agregar)[coluna_somar]
                .sum()
                .astype(int)  # força para inteiro
                .sort_values(ascending=False)
            )

            return resultados

        except Exception as e:
            logger.error(f"Erro ao agregar e somar por grupo: {e}", exc_info=True)
            raise

    def filtrar_tempestividade(self, df):
        df = df.copy()
        df["tipo"] = df["tipo"].astype(str).str.lower().str.strip()

        return df[df["tipo"].str.contains(r"tempestiv", na=False)]
