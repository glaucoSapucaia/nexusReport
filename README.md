# 📊 GMCAT Nexuscore – Relatório de Dados

Este projeto gera **relatórios automáticos em PDF** com **gráficos de agregação** sobre dados de **protocolos, rotas e vistorias** da base GMCAT Nexuscore.

O relatório consolida as informações em um único arquivo visual, facilitando a análise de desempenho e acompanhamento das atividades.

## ⚙️ Funcionalidades

- Conexão automática ao banco PostgreSQL via `.env`
- Filtragem de dados por período (`data_inicio`, `data_fim`)
- Agregações automáticas (`value_counts`, somas por grupo)
- Geração de gráficos com **Matplotlib**
- Criação de **PDF consolidado** com:
  - Página de título
  - Índice
  - Seções de Protocolos, Rotas e Vistorias
  - Data e hora de geração


## 🚀 Execução

### 1. Crie o arquivo `.env`
Defina as credenciais de banco de dados:

- DB_USER=seu_usuario
- DB_PASSWORD=sua_senha
- DB_HOST=seu_host
- DB_PORT=sua_porta
- DB_NAME=seu_db


### 2. Instale as dependências e execute
```bash
pip install -r requirements.txt
python main.py
```

## 🧠 Principais Tecnologias

- Python 3.11+
- Matplotlib
- Pandas
- SQLAlchemy
- Psycopg2
- dotenv (configurações seguras)
- PostgreSQL