import logging


class AgentLogger(object):
    logger = logging.getLogger("agents_crawler")
    logger.setLevel(logging.DEBUG)

    # create file handler
    file_handler = logging.FileHandler('crawler.log')
    file_handler.setLevel(logging.INFO)

    # create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
