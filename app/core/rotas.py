from .analyzer import DBAnalyzer

analisador = DBAnalyzer()

# Carrega apenas a tabela de protocolos
dfs = analisador.carregar_tabelas(["rotas_tb"])

# Filtra último trimestre
df_trimestre = analisador.filtrar_periodo("rotas_tb", "data_geracao")

# Agregações desejadas
colunas_agregacao = [
    "grupo",
    "status",
]

resultados = analisador.agregacoes(df_trimestre, colunas_agregacao)

# Mostra resultados
for coluna, resumo in resultados.items():
    print(f"\nAgregação por {coluna}:")
    print(resumo)
