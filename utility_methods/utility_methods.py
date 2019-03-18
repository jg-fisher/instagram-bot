import configparser
import functools
import logging
import time


def init_config(config_file_path):
    """
    Initializes the configuration

    Args:
        config_file_path:str: Path to .ini configuration file
    """

    # asserting configuration file has the correct extension
    path = config_file_path.split('.')
    assert(path[len(path)-1] == 'ini')

    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config


def get_logger(logger_file_path):
    """
    Creates a logging object and returns it

    Returns:
        logger:logging.Log: Log object
    """

    logger = logging.getLogger('InstaBotLogger')
    logger.setLevel(logging.DEBUG)
 
    # log file handler
    fh = logging.FileHandler(logger_file_path)
 
    # log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
 
    logger.addHandler(fh)
    return logger
 
 
def exception(func):
    """
    Exception logging decorator

    Args:
        func:function: Function to wrap

    Returns:
        wrapper:function: Wrapper function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            # log the exception
            msg = "Exception in method {}".format(func.__name__)
            logger = get_logger('bot.log')
            logger.exception(msg)
 
    return wrapper


def insta_method(func):
    """
    Instagram method decorator. Sleeps for 2 seconds before and after calling any methods that interact with Instagram.

    Args:
        func:function: Function to wrap

    Returns:
        wrapper:function: Wrapper function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(2)
        func(*args, **kwargs)
        time.sleep(2)

    return wrapper