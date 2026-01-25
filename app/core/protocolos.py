from .analyzer import DBAnalyzer
from utils import logger

logger.info("Iniciando pipeline de protocolos.")

try:
    analisador = DBAnalyzer()

    # Carrega apenas a tabela de protocolos
    logger.info("Carregando tabela 'protocolos_gmcat_tb'")
    dfs = analisador.carregar_tabelas(["protocolos_gmcat_tb"])

    # Filtra periodo
    logger.info("Aplicando filtro de período.")
    df_periodo = analisador.filtrar_periodo(
        "protocolos_gmcat_tb", "data_cadastro_gerencia"
    )

    # Agregações desejadas
    colunas_agregacao = [
        "tipo",
        "status",
        "regional",
        "grupo",
        "numero_de_vistorias",
        "pontuacao_resolucao",
        "tempo_servico",
    ]
    logger.info(f"Realizando agregações para colunas: {colunas_agregacao}")

    # Resultados gerais
    resultados = analisador.agregacoes(df_periodo, colunas_agregacao)

    # Tempo de serviço por grupo
    resultados_grupo_tempo_servico = analisador.agregacao_soma_por_grupo(
        df_periodo, "grupo", "tempo_servico"
    )

    # Isolamento de protocolos tempestivos e intempestivos
    df_tempestivo = analisador.filtrar_tempestividade(df_periodo)
    resultados_tempestivo_intempestivo = analisador.agregacoes(df_tempestivo, ["tipo"])

    logger.info("Pipeline de análise de protocolos concluído com sucesso.")

except Exception as e:
    logger.error(f"Erro no pipeline de análise de protocolos: {e}", exc_info=True)
    raise
