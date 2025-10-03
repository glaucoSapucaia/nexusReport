from .analyzer import DBAnalyzer
from utils import logger

logger.info("Iniciando pipeline de rotas.")

try:
    analisador = DBAnalyzer()

    # Carrega apenas a tabela de rotas
    logger.info("Carregando tabela 'rotas_tb'")
    dfs = analisador.carregar_tabelas(["rotas_tb"])

    # Filtra periodo
    logger.info("Aplicando filtro de período.")
    df_periodo = analisador.filtrar_periodo("rotas_tb", "data_geracao")
    logger.info(f"Após filtro: {len(df_periodo)} registros restantes.")

    # Agregações desejadas
    colunas_agregacao = ["grupo", "status"]
    logger.info(f"Realizando agregações para colunas: {colunas_agregacao}")
    resultados = analisador.agregacoes(df_periodo, colunas_agregacao)

    logger.info("Pipeline de análise de rotas concluído com sucesso.")

except Exception as e:
    logger.error(f"Erro no pipeline de análise de rotas: {e}", exc_info=True)
    raise
