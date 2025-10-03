from pipeline import gerar_relatorio_agregacao
from utils import logger

if __name__ == "__main__":
    logger.info("Iniciando execução do programa.")

    try:
        logger.info("Chamando função principal: gerar_relatorio_agregacao()")
        gerar_relatorio_agregacao()
        logger.info("Execução concluída com sucesso.")

    except Exception as e:
        logger.error(f"Falha durante a execução: {e}", exc_info=True)
        raise
