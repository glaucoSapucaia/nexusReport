from .analyzer import DBAnalyzer

analisador = DBAnalyzer()

# Carrega apenas a tabela de protocolos
dfs = analisador.carregar_tabelas(["pontos_visitados_tb"])

# Filtra último trimestre
df_trimestre = analisador.filtrar_periodo("pontos_visitados_tb", "data_registro")

# Agregações desejadas
colunas_agregacao = [
    "resultado",
    "responsavel",
]

resultados = analisador.agregacoes(df_trimestre, colunas_agregacao)

# Mostra resultados
for coluna, resumo in resultados.items():
    print(f"\nAgregação por {coluna}:")
    print(resumo)
