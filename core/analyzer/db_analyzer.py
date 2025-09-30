import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from datetime import datetime


class DBAnalyzer:
    def __init__(self, env_path=".env"):
        load_dotenv(env_path)
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")

        # Cria a engine SQLAlchemy
        self.engine = create_engine(
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )
        self.inspector = inspect(self.engine)
        self.dfs = {}

    def carregar_tabelas(self, tabelas):
        """Carrega tabelas do banco para DataFrames"""
        for tabela in tabelas:
            if tabela in self.inspector.get_table_names(schema="public"):
                self.dfs[tabela] = pd.read_sql_table(
                    tabela, self.engine, schema="public"
                )
                print(f"Tabela {tabela} carregada com {len(self.dfs[tabela])} linhas")
            else:
                print(f"Tabela {tabela} não encontrada no banco")
        return self.dfs

    def filtrar_ultimo_trimestre(self, tabela, coluna_data="data_cadastro_gerencia"):
        """Filtra registros do último trimestre"""
        df = self.dfs.get(tabela)
        if df is None:
            raise ValueError(f"Tabela {tabela} não carregada.")
        df[coluna_data] = pd.to_datetime(df[coluna_data])
        hoje = datetime.today()
        ultimo_trimestre = hoje - pd.DateOffset(months=3)
        return df[df[coluna_data] >= ultimo_trimestre]

    def agregacoes(self, df, colunas):
        """Realiza agregações simples (value_counts) para várias colunas,
        remove NaN e converte valores para int."""
        resultados = {}
        for coluna in colunas:
            # Conta ocorrências
            vc = df[coluna].value_counts(dropna=True)  # remove NaN
            # Converte index numérico para int quando possível
            if pd.api.types.is_float_dtype(vc.index):
                vc.index = vc.index.astype(int)
            resultados[coluna] = vc
        return resultados
