import os

import logging
import colorlog

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Config class to set different variables

    Args:
        object (object): The most base type
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'saturn'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'fr']


def init_logger(dunder_name, testing_mode):
    """Instantiate a logger so as to log message

    Args:
        dunder_name (string): name of the logger
        testing_mode (bool): indicates wether to use Debug or not

    Returns:
        Logger: A logger with the specified name
    """
    log_format = ('[%(levelname)s] - %(asctime)s - %(message)s')
    bold_seq = '\033[1m'
    colorlog_format = '{} %(log_color)s {}'.format(bold_seq,log_format)
    colorlog.basicConfig(format=colorlog_format)
    logger = logging.getLogger(dunder_name)

    if testing_mode:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Output full log
    # fh = logging.FileHandler('app.log')
    # fh.setLevel(logging.DEBUG)
    # formatter = logging.Formatter(log_format)
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)

    # Output warning log
    # fh = logging.FileHandler('app.warning.log')
    # fh.setLevel(logging.WARNING)
    # formatter = logging.Formatter(log_format)
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)

    # Output error log
    # fh = logging.FileHandler('app.error.log')
    # fh.setLevel(logging.ERROR)
    # formatter = logging.Formatter(log_format)
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)

    return logger
