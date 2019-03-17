import configparser
import functools
import logging
import time


def init_config(config_file_path):
    """
    Initializes the configuration>
    """
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config


def init_logger(logger_file_path):
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger('IGBotLogger')
    logger.setLevel(logging.INFO)
 
    # create the logging file handler
    fh = logging.FileHandler(logger_file_path)
 
    # log output format
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    logger.addHandler(fh)
    return logger
 
 
def exception(func):
    """
    Exception logging decorator
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            # log the exception
            msg = "There was an exception in {}".format(func.__name__)
            logger.exception(msg)
 
            # re-raise the exception
            raise
    return wrapper


def insta_method(func):
    """
    Instagram method decorator
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        time.sleep(2)

    return wrapper