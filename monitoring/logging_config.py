import logging


def setup_logger():

    logger = logging.getLogger("rag")

    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("logs/rag.log")

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger