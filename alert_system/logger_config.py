import logging


def setup_logger(name) -> logging.Logger:
    """
    method for creation a local logger
    :param name:
    :return:
    """
    FORMAT = "[%(name)s %(module)s:%(lineno)s]\n\t %(message)s \n"
    TIME_FORMAT = "%d.%m.%Y %I:%M:%S %p"

    logging.basicConfig(
        format=FORMAT, datefmt=TIME_FORMAT, level=logging.DEBUG, filename="log-file-name2.log"
    )

    logger = logging.getLogger(name)
    return logger
