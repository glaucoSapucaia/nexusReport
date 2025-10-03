from .analyzer import DBAnalyzer
from utils import logger

logger.info("Iniciando pipeline de pontos visitados.")

try:
    analisador = DBAnalyzer()

    # Carrega apenas a tabela de pontos visitados
    logger.info("Carregando tabela 'pontos_visitados_tb'")
    dfs = analisador.carregar_tabelas(["pontos_visitados_tb"])

    # Filtra periodo
    logger.info("Aplicando filtro de período.")
    df_periodo = analisador.filtrar_periodo("pontos_visitados_tb", "data_registro")
    logger.info(f"Após filtro: {len(df_periodo)} registros restantes.")

    # Agregações desejadas
    colunas_agregacao = ["resultado", "responsavel"]
    logger.info(f"Realizando agregações para colunas: {colunas_agregacao}")
    resultados = analisador.agregacoes(df_periodo, colunas_agregacao)

    logger.info("Pipeline de pontos visitados concluído com sucesso.")

except Exception as e:
    logger.error(f"Erro no pipeline de análise: {e}", exc_info=True)
    raise
