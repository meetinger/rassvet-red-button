import logging


def get_logger(name: str = "bot_logger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(name)s - %(module)s:%(lineno)d - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("bot.log", mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger