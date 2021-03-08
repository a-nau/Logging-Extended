import os

import logging_extended as logging

standard_loglevel_dict = {
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'DEBUG': 10,
}

new_loglevel_dict = {
    'VERBOSE': 5,
    'TRACK': 25,
    'CONFIG': 56
}


def test_default():
    """
    Example using the default settings
    """
    logger = logging.getLogger(__name__)
    log_all_levels(logger)
    log_all_levels_decorated(logger)
    log_all_levels_loop(logger)
    return logger


def test_basicConfig():
    """
    Example setting a new config with basicConfig
    """
    logging_config = {
        'format': '%(asctime)s [%(levelname)s]: %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
        'level': 5,  # info (see https://docs.python.org/3/library/logging.html#logging-levels)
    }
    logging.basicConfig(**logging_config)
    logging.setGitConfig({"auto_commit": False})
    logger = logging.getLogger(__name__)
    log_all_levels(logger)
    log_all_levels_decorated(logger)
    log_all_levels_loop(logger)
    return logger


def test_dictConfig():
    """
    Example setting a new config with a dict
    """
    log_level = 1
    logging_config = dict(
        version=1,
        disable_existing_loggers=False,
        formatters={
            'f': {
                'format': '[%(asctime)s] - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        handlers={
            'h': {'class': 'logging.StreamHandler',
                  'formatter': 'f',
                  'level': log_level}
        },
        root={
            'handlers': ['h'],
            'level': log_level,
        },
    )

    logging.config.dictConfig(logging_config)
    logger = logging.getLogger(__name__)
    log_all_levels(logger)
    log_all_levels_decorated(logger)
    log_all_levels_loop(logger)
    return logger


def test_add_file_handler():
    """
    Example adding a log file
    """
    change_cwd()
    logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler('logging.log')
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    log_all_levels(logger)
    log_all_levels_decorated(logger)
    log_all_levels_loop(logger)
    return logger


def test_load_config_from_file():
    """
    Example setting new config with `.ini` file
    """
    change_cwd()
    path_config_file = os.path.join("logging_extended", "logging_config.ini")
    if not os.path.exists(path_config_file):
        raise FileNotFoundError(f"File {path_config_file} not found!")
    logging.config.fileConfig(path_config_file)
    logger = logging.getLogger(__name__)
    log_all_levels(logger)
    log_all_levels_decorated(logger)
    log_all_levels_loop(logger)
    return logger


def log_all_levels(logger_instance):
    """
    Write test log for all levels
    """
    for log_level in list(new_loglevel_dict.keys()) + list(standard_loglevel_dict.keys()):
        getattr(logger_instance, log_level.lower())('test ' + log_level)


def log_all_levels_decorated(logger_instance):
    """
    Write decorated test log for all levels
    """
    for log_level in list(new_loglevel_dict.keys()) + list(standard_loglevel_dict.keys()):
        getattr(logger_instance, log_level.lower())('test ' + log_level, decorated=True)
    getattr(logger_instance, "info")("", decorated=True)


def log_all_levels_loop(logger_instance):
    """
    Write test log for loops on all levels
    """
    for log_level in list(new_loglevel_dict.keys()) + list(standard_loglevel_dict.keys()):
        for i in range(3):
            logger_instance.loop_counter("test", i, getattr(logging, log_level.upper()))
        getattr(logger_instance, log_level.lower())("\n\n")


def change_cwd():
    path_base = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2])
    os.chdir(path_base)


if __name__ == '__main__':
    test_default()
    test_basicConfig()
    test_dictConfig()
    test_add_file_handler()
    test_load_config_from_file()
