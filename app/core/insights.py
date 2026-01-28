import pandas as pd
from .analyzer import DBAnalyzer
from utils import logger

logger.info("Iniciando pipeline de insights.")

try:
    analisador = DBAnalyzer()
    dfs = analisador.carregar_tabelas(["protocolos_gmcat_tb"])
    df_insights = dfs["protocolos_gmcat_tb"].copy()

    coluna_inicio = 'data_cadastro_sigede'
    coluna_fim = 'data_resolucao' 

    if coluna_fim in df_insights.columns:
        df_insights[coluna_inicio] = pd.to_datetime(df_insights[coluna_inicio]).dt.tz_localize(None)
        df_insights[coluna_fim] = pd.to_datetime(df_insights[coluna_fim]).dt.tz_localize(None)
        df_insights["tempo_resolucao"] = (df_insights[coluna_fim] - df_insights[coluna_inicio]).dt.days
        df_insights = df_insights.dropna(subset=["tempo_resolucao"])
        
        # Criamos o objeto que o seu __init__.py está tentando importar
        resultados_insights = {"df": df_insights}
        
        logger.info(f"Pipeline de insights concluído. {len(df_insights)} registros processados.")
    else:
        logger.error(f"Coluna {coluna_fim} não encontrada.")
        df_insights = pd.DataFrame(columns=["tempo_resolucao"])
        resultados_insights = {"df": df_insights}

except Exception as e:
    logger.error(f"Erro no pipeline de insights: {e}", exc_info=True)
    raise