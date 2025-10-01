from .analyzer import DBAnalyzer

analisador = DBAnalyzer()

# Carrega apenas a tabela de protocolos
dfs = analisador.carregar_tabelas(["protocolos_gmcat_tb"])

# Filtra último trimestre
df_trimestre = analisador.filtrar_periodo(
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

resultados = analisador.agregacoes(df_trimestre, colunas_agregacao)

# Mostra resultados
for coluna, resumo in resultados.items():
    print(f"\nAgregação por {coluna}:")
    print(resumo)
