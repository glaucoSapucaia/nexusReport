import logging

# Cria logger central
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# Evita duplicar handlers se este módulo for importado várias vezes
if not logger.handlers:
    # Handler de arquivo
    file_handler = logging.FileHandler("app_log.txt", mode="w", encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # Formato do log
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Opcional: também exibir no console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
