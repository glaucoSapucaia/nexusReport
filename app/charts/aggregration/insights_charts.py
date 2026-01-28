from utils import logger
import pandas as pd
import matplotlib.pyplot as plt
# Importa o dataframe processado do core/insights.py
from core.insights import df_insights as df

def _configurar_e_salvar(titulo, pdf):
    """
    Função auxiliar para aplicar título, ajustar layout e salvar no PDF.
    """
    plt.title(titulo)
    plt.suptitle("")
    plt.tight_layout()
    if pdf:
        pdf.savefig()
    plt.close()

def gerar_graficos_insights(pdf=None):
    """
    Gera gráficos de insights para o relatório.
    """
    logger.info("Iniciando geração de gráficos de insights.")

    # Verifica se o dataframe não está vazio para evitar erros de plotagem
    if df.empty:
        logger.warning("DataFrame de insights está vazio. Pulando geração de gráficos.")
        return

    try:
        # 1. Histograma tempo médio de resolução
        logger.info("Gerando gráfico: Distribuição do Tempo de Resolução")
        plt.figure(figsize=(12, 8))
        
        # Filtra valores nulos apenas por segurança antes de plotar
        dados_resolucao = df["tempo_resolucao"].dropna()
        
        plt.hist(dados_resolucao, bins=20, color='skyblue', edgecolor='black')
        
        media = dados_resolucao.mean()
        plt.axvline(media, color='red', linestyle='dashed', label=f'Média: {media:.2f} dias')
        
        plt.xlabel("Dias para Resolução")
        plt.ylabel("Quantidade de Protocolos")
        plt.legend()
        _configurar_e_salvar("Tempo médio de resolução (Distribuição)", pdf)


        # 2. Boxplot Geral (Outliers)
        logger.info("Gerando gráfico: Análise de Outliers de Tempo")
        plt.figure(figsize=(12, 8))
        
        plt.boxplot(dados_resolucao, vert=False, patch_artist=True, 
                    boxprops=dict(facecolor='lightgreen'))
        
        plt.xlabel("Dias para Resolução")
        _configurar_e_salvar("Tempo médio de resolução (Análise de Outliers)", pdf)

        # 3. Prioridade vs Tempo 
        if 'prioridade' in df.columns:
            df_prio = df.dropna(subset=['prioridade', 'tempo_resolucao'])
            if not df_prio.empty:
                logger.info("Gerando gráfico: Prioridade vs Tempo Real")
                
                plt.figure(figsize=(12, 8))
                ax = plt.gca() # Pega o eixo atual
                
                df_prio.boxplot(
                    column='tempo_resolucao', 
                    by='prioridade', 
                    vert=False, 
                    patch_artist=True, 
                    ax=ax
                )
                
                plt.xlabel("Dias para Resolução")
                plt.ylabel("Prioridade")
                
                # Chamada da função auxiliar
                _configurar_e_salvar("Prioridade Declarada vs Tempo Real", pdf)

        # 4. Volume ao Longo do Tempo
        logger.info("Gerando gráfico: Volume de Protocolos ao Longo do Tempo")
        df_tempo = df.copy()
        df_tempo["data_ref"] = pd.to_datetime(df_tempo[["data_cadastro_sigede", "data_cadastro_gerencia"]].min(axis=1)).dt.date
        contagem = df_tempo.groupby("data_ref").size()
        plt.figure(figsize=(12, 8))
        plt.plot(contagem.index, contagem.values, marker='o', color='#2E8B57')
        plt.xticks(rotation=45)
        _configurar_e_salvar("Volume de Protocolos ao Longo do Tempo", pdf)

       # 5. Boxplot por Tipo
        logger.info("Gerando gráfico: Tempo de Resolução por Tipo")
        # Filtrando nulos para garantir que o gráfico seja gerado corretamente
        df_tipo = df.dropna(subset=['tipo', 'tempo_resolucao'])
        
        if not df_tipo.empty:
            plt.figure(figsize=(12, 10)) 
            ax = plt.gca()
            
            df_tipo.boxplot(
                column='tempo_resolucao', 
                by='tipo', 
                vert=False, 
                patch_artist=True, 
                ax=ax
            )
            
            plt.xlabel("Dias para Resolução")
            plt.ylabel("Tipo de Protocolo")
            
            
            plt.suptitle("") 
            
            _configurar_e_salvar("Tempo de Resolução por Tipo", pdf)

            # 6. Mapa Geográfico (Scatter Plot)
            logger.info("Gerando gráfico: Concentração Geográfica")
            df_geo = df.dropna(subset=['latitude', 'longitude']).copy()
        
            if not df_geo.empty:
                plt.figure(figsize=(12, 8))
            
                # Criando o gráfico de dispersão
                plt.scatter(
                df_geo['longitude'], 
                df_geo['latitude'], 
                alpha=0.4, 
                c='blue',
                edgecolors='w'
            )
            
            plt.xlabel("Longitude")
            plt.ylabel("Latitude")
            plt.grid(True, linestyle='--', alpha=0.6)
            
            # Chamada da função auxiliar (sem o parâmetro fig)
            _configurar_e_salvar("Concentração Geográfica de Protocolos", pdf)

            # 7. Pontuação (Prioridade vs Resolução)
        logger.info("Gerando gráfico: Pontuação de Prioridade vs Resolução")
        # Removemos nulos para evitar que o gráfico fique em branco ou dê erro
        df_scores = df.dropna(subset=['pontuacao_prioridade', 'pontuacao_resolucao'])
        
        if not df_scores.empty:
            plt.figure(figsize=(12, 8))
            
            # Criando o scatter plot
            plt.scatter(
                df_scores['pontuacao_prioridade'], 
                df_scores['pontuacao_resolucao'], 
                alpha=0.5, 
                color='orange',
                edgecolors='k' # Adiciona uma borda preta fina nos pontos para melhor visibilidade
            )
            
            # Legendas essenciais para análise
            plt.xlabel("Pontuação de Prioridade (Planejado)")
            plt.ylabel("Pontuação de Resolução (Executado)")
            plt.grid(True, linestyle=':', alpha=0.6)
            
            # Chamada correta da função (sem o parâmetro fig)
            _configurar_e_salvar("Correlação: Prioridade Planejada vs Pontuação de Resolução", pdf)

            # 8. Tamanho da Reclamação vs Tempo
        # Agora que calculamos no core, esta condição será verdadeira
        if 'tamanho_reclamacao' in df.columns:
            logger.info("Gerando gráfico: Tamanho da Reclamação vs Tempo")
            
            # Removemos nulos para garantir a dispersão correta
            df_rec = df.dropna(subset=['tamanho_reclamacao', 'tempo_resolucao'])
            
            if not df_rec.empty:
                plt.figure(figsize=(12, 8))
                
                plt.scatter(
                    df_rec['tamanho_reclamacao'], 
                    df_rec['tempo_resolucao'], 
                    alpha=0.5, 
                    color='purple',
                    edgecolors='w'
                )
                
                plt.xlabel("Tamanho da Reclamação (Nº de Caracteres)")
                plt.ylabel("Dias para Resolução")
                plt.grid(True, linestyle='--', alpha=0.5)
                
                # Chamada correta (sem o parâmetro fig)
                _configurar_e_salvar("Correlação: Complexidade do Texto vs Tempo de Resolução", pdf)


        logger.info("Finalizada a geração dos gráficos de insights.")

    except Exception as e:
        logger.error(f"Erro ao gerar gráficos de insights: {e}", exc_info=True)
        raise