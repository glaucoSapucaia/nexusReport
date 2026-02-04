import pandas as pd
import plotly.express as px
from .analyzer import DBAnalyzer
from utils import logger

def buscar_regional_por_coordenada(lat, lon):
    if pd.isna(lat) or pd.isna(lon):
        return None
    
    # Bounding Boxes (caixas de coordenadas) das Regionais oficiais de BH
    if -19.990 <= lat <= -19.850 and -44.020 <= lon <= -43.950: return "BARREIRO"
    if -19.880 <= lat <= -19.750 and -43.980 <= lon <= -43.900: return "VENDA NOVA"
    if -19.870 <= lat <= -19.800 and -44.020 <= lon <= -43.950: return "PAMPULHA"
    if -19.940 <= lat <= -19.900 and -43.950 <= lon <= -43.910: return "CENTRO-SUL"
    if -19.930 <= lat <= -19.880 and -43.920 <= lon <= -43.870: return "LESTE"
    if -19.910 <= lat <= -19.850 and -43.950 <= lon <= -43.910: return "NORDESTE"
    if -19.880 <= lat <= -19.820 and -43.950 <= lon <= -43.900: return "NORTE"
    if -19.960 <= lat <= -19.910 and -44.010 <= lon <= -43.950: return "OESTE"
    if -19.930 <= lat <= -19.880 and -43.980 <= lon <= -43.930: return "NOROESTE"
    return None

logger.info("Iniciando pipeline de insights.")
df_insights = pd.DataFrame()
resultados_insights = {}

try:
    analisador = DBAnalyzer()
    dfs = analisador.carregar_tabelas(["protocolos_gmcat_tb"])

    coluna_inicio = 'data_cadastro_sigede'
    coluna_fim = 'data_resolucao' 

    df_insights = analisador.filtrar_periodo("protocolos_gmcat_tb", coluna_inicio)

    if not df_insights.empty:
        # --- LÓGICA DE RECUPERAÇÃO DE REGIONAL ---
        
        # 1. Padroniza para maiúsculo para evitar "Barreiro" vs "BARREIRO"
        df_insights['regional'] = df_insights['regional'].astype(str).str.upper().str.strip()

        # 2. Identifica onde a regional está faltando ou é inválida
        termos_vazios = ['NAN', 'NONE', 'SEM REGIONAL', '0', '', 'N/A']
        mask_invalida = df_insights['regional'].isin(termos_vazios)

        # 3. Tenta preencher APENAS onde está inválido usando a função de GPS
        logger.info(f"Analisando {mask_invalida.sum()} registros sem regional definida...")
        
        df_insights.loc[mask_invalida, 'regional'] = df_insights[mask_invalida].apply(
            lambda x: buscar_regional_por_coordenada(x['latitude'], x['longitude']) or x['regional'], 
            axis=1
        )

        # 4. Limpeza final: o que continuou inválido vira "SEM REGIONAL" padronizado
        df_insights.loc[df_insights['regional'].isin(termos_vazios), 'regional'] = 'SEM REGIONAL'

    if coluna_fim in df_insights.columns:
        df_insights[coluna_inicio] = pd.to_datetime(df_insights[coluna_inicio]).dt.tz_localize(None)
        df_insights[coluna_fim] = pd.to_datetime(df_insights[coluna_fim]).dt.tz_localize(None)
        df_insights["tempo_resolucao"] = (df_insights[coluna_fim] - df_insights[coluna_inicio]).dt.days
        df_insights['tamanho_reclamacao'] = df_insights['reclamacao'].str.len().fillna(0)
        df_mapa = df_insights.dropna(subset=['latitude', 'longitude']).copy()

        if not df_mapa.empty:
            # 2. Mapa de Dispersão COLORIDO POR TIPO (conforme sua ideia)
            fig_dispersao = px.scatter_mapbox(
                df_mapa, 
                lat="latitude", lon="longitude",
                hover_name="tipo", 
                color="tipo", # <--- MUDANÇA AQUI (era regional)
                zoom=10, 
                center={"lat": -19.9167, "lon": -43.9333},
                mapbox_style="carto-darkmatter", # Estilo escuro que você gostou
                title="Distribuição Geográfica por Tipo de Demanda"
            )

            # 3. Mapa de Calor (Heatmap)
            fig_calor = px.density_mapbox(
                df_mapa, lat="latitude", lon="longitude",
                radius=10, zoom=10, center={"lat": -19.9167, "lon": -43.9333},
                mapbox_style="carto-darkmatter", title="Concentração de Demandas"
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