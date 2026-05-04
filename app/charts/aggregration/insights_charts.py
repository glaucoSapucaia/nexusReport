from utils import logger
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx
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

        # 3. Prioridade vs Tempo (AJUSTADO PARA CLAREZA)
        if 'prioridade' in df.columns:
            # Filtramos apenas quem tem tempo calculado (processos concluídos)
            df_prio = df.dropna(subset=['prioridade', 'tempo_resolucao'])
            
            if not df_prio.empty:
                logger.info("Gerando gráfico: Prioridade vs Tempo Real")
                
                # Tamanho padrão igual às outras páginas
                plt.figure(figsize=(12, 8))
                ax = plt.gca() 
                
                # --- O PULO DO GATO ---
                # showfliers=False: remove os pontos de erro que esticam o gráfico
                # patch_artist=True: permite colorir as caixas
                df_prio.boxplot(
                    column='tempo_resolucao', 
                    by='prioridade', 
                    vert=False, 
                    patch_artist=True, 
                    showfliers=False, 
                    ax=ax,
                    boxprops=dict(facecolor='#ffcc80', color='#e65100'), # Laranja suave
                    medianprops=dict(color='red', linewidth=2)
                )
                
                # Título que explica o dado para o seu chefe
                concluidos = len(df_prio)
                total_mes = len(df)
                plt.title(f"Eficiência por Prioridade - Janeiro/2026\n(Análise de {concluidos} de {total_mes} protocolos concluídos)", 
                          fontsize=14, fontweight='bold')
                
                plt.xlabel("Dias para Resolução (Excluindo casos atípicos)")
                plt.ylabel("Prioridade Declarada")
                plt.suptitle("") # Remove o título automático duplicado do Pandas
                plt.grid(axis='x', linestyle='--', alpha=0.3)
                
                _configurar_e_salvar("Prioridade vs Tempo de Atendimento", pdf)

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

        # 6. Distribuição Regional (Volume por Regional)
        logger.info("Gerando gráfico: Distribuição por Regional (Barra)")
        if 'regional' in df.columns:
            plt.figure(figsize=(12, 8))
            
            # Conta protocolos por regional e ordena do maior para o menor
            dist_regional = df['regional'].value_counts().sort_values(ascending=True)
            
            # Cores variadas para cada barra
            cores = plt.cm.viridis(np.linspace(0, 1, len(dist_regional)))
            
            dist_regional.plot(kind='barh', color=cores, edgecolor='black', alpha=0.7)
            
            plt.title("Volume de Protocolos por Regional - Janeiro/2026", fontsize=14, fontweight='bold')
            plt.xlabel("Quantidade de Protocolos")
            plt.ylabel("Regional")
            plt.grid(axis='x', linestyle='--', alpha=0.6)
            
            # Adiciona os números no final de cada barra
            for i, v in enumerate(dist_regional):
                plt.text(v + 0.5, i, str(v), color='black', va='center', fontweight='bold')
            
            _configurar_e_salvar("Distribuição por Regional (Volume)", pdf)

        # 6.1 Mapa de Dispersão - AJUSTE DE TAMANHO
        logger.info("Gerando mapa...")
        df_geo = df.dropna(subset=['latitude', 'longitude', 'tipo']).copy()
    
        if not df_geo.empty:
            # Isso garante que esta página tenha o mesmo tamanho das outras
            fig, ax = plt.subplots(figsize=(12, 8)) 
            
            tipos = sorted(df_geo['tipo'].unique())
            cores_mapa = plt.cm.get_cmap('tab10', len(tipos))
            
            for i, tipo in enumerate(tipos):
                mask = df_geo['tipo'] == tipo
                ax.scatter(
                    df_geo.loc[mask, 'longitude'], 
                    df_geo.loc[mask, 'latitude'], 
                    label=tipo,
                    alpha=0.8,      
                    edgecolors='black', 
                    linewidth=0.7,   
                    s=70, # Diminuído levemente para o novo tamanho de página
                    color=cores_mapa(i)
                )
            
            # Fundo de contraste (OpenStreetMap)
            try:
                ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)
            except:
                ax.set_facecolor('white')

            # Enquadramento BH
            ax.set_xlim(-44.10, -43.85) 
            ax.set_ylim(-20.05, -19.75) 
            ax.set_axis_off()
            
            # --- LEGENDA: Agora ajustada para caber no A4 sem empurrar a margem ---
            plt.legend(
                title="Tipos de Protocolo", 
                loc='center left', 
                bbox_to_anchor=(1.02, 0.5), # Posiciona logo à direita do gráfico
                frameon=True, 
                shadow=True, 
                fontsize=11,          
                title_fontsize=13,    
                markerscale=1.3,      
                borderpad=1.2,        
                labelspacing=1.0      
            )
            
            plt.title("Distribuição por Tipo - Belo Horizonte (Jan/2026)", 
                      fontsize=16, fontweight='bold', color='black', pad=20)
            
            fig.patch.set_facecolor('white')
            
            plt.tight_layout(rect=[0, 0, 0.85, 1]) 
            
            _configurar_e_salvar("Mapa de Demandas por Tipo", pdf)

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