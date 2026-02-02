import pandas as pd
import plotly.express as px
from .analyzer import DBAnalyzer
from utils import logger

logger.info("Iniciando pipeline de insights.")

try:
    analisador = DBAnalyzer()
    dfs = analisador.carregar_tabelas(["protocolos_gmcat_tb"])

    coluna_inicio = 'data_cadastro_sigede'
    coluna_fim = 'data_resolucao' 

    df_insights = analisador.filtrar_periodo("protocolos_gmcat_tb", coluna_inicio)

    if coluna_fim in df_insights.columns:
        df_insights[coluna_inicio] = pd.to_datetime(df_insights[coluna_inicio]).dt.tz_localize(None)
        df_insights[coluna_fim] = pd.to_datetime(df_insights[coluna_fim]).dt.tz_localize(None)
        df_insights["tempo_resolucao"] = (df_insights[coluna_fim] - df_insights[coluna_inicio]).dt.days
        df_insights = df_insights.dropna(subset=["tempo_resolucao"])
        df_insights['tamanho_reclamacao'] = df_insights['reclamacao'].str.len().fillna(0)
        if not df_insights.empty:
    # 1. Preparar os dados para o mapa (remover coordenadas vazias)
            df_mapa = df_insights.dropna(subset=['latitude', 'longitude'])

    # 2. Criar o Mapa de Dispersão
            fig_dispersao = px.scatter_mapbox(
                df_mapa, lat="latitude", lon="longitude",
                hover_name="tipo", color="regional",
                zoom=10, center={"lat": -19.9167, "lon": -43.9333},
                mapbox_style="carto-positron", title="Dispersão de Protocolos"
            )

    # 3. Criar o Mapa de Calor
            fig_calor = px.density_mapbox(
                df_mapa, lat="latitude", lon="longitude",
                radius=10, zoom=10, center={"lat": -19.9167, "lon": -43.9333},
                mapbox_style="stamen-terrain", title="Concentração de Demandas"
            )

    # 4. Adicionar ao dicionário de resultados
            resultados_insights = {
                "df": df_insights,
                "mapa_dispersao": fig_dispersao,
                "mapa_calor": fig_calor
            }
        
        
        logger.info(f"Pipeline de insights concluído. {len(df_insights)} registros processados.")
    else:
        logger.error(f"Coluna {coluna_fim} não encontrada.")
        df_insights = pd.DataFrame(columns=["tempo_resolucao"])
        resultados_insights = {"df": df_insights}

except Exception as e:
    logger.error(f"Erro no pipeline de insights: {e}", exc_info=True)
    raise