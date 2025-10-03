import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from utils import logger

data_inicio = "2025-09-01"
data_fim = "2025-09-30"


class DBAnalyzer:
    def __init__(self, env_path=".env"):
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
        logger.info(f"Carregando tabelas: {tabelas}")
        for tabela in tabelas:
            try:
                if tabela in self.inspector.get_table_names(schema="public"):
                    self.dfs[tabela] = pd.read_sql_table(
                        tabela, self.engine, schema="public"
                    )
                    logger.info(
                        f"Tabela '{tabela}' carregada com {len(self.dfs[tabela])} linhas"
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
        logger.info(
            f"Filtrando registros da tabela '{tabela}' pelo período {self.data_inicio} até {self.data_fim}"
        )

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

        logger.info(f"Filtro aplicado. {len(df)} registros restantes.")
        return df

    def agregacoes(self, df, colunas, top_n=None):
        """
        Realiza agregações simples (value_counts) para várias colunas,
        remove NaN e converte valores para int.
        """
        logger.info(f"Iniciando agregações para colunas: {colunas}, top_n={top_n}")
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
                logger.debug(
                    f"Agregação concluída para coluna '{coluna}': {len(vc)} categorias"
                )

            except Exception as e:
                logger.error(f"Erro ao agregar coluna {coluna}: {e}", exc_info=True)
                raise

        logger.info("Agregações concluídas com sucesso.")
        return resultados
