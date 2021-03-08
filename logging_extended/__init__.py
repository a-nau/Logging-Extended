from logging import *
from logging import config

__all__ = ['BASIC_FORMAT', 'CRITICAL', 'DEBUG', 'ERROR',
           'FATAL', 'FileHandler', 'Filter', 'Formatter', 'Handler', 'INFO',
           'LogRecord', 'Logger', 'LoggerAdapter', 'NOTSET', 'NullHandler',
           'StreamHandler', 'WARN', 'WARNING', 'addLevelName', 'basicConfig',
           'captureWarnings', 'critical', 'debug', 'disable', 'error',
           'exception', 'fatal', 'getLevelName', 'getLogger', 'getLoggerClass',
           'info', 'log', 'makeLogRecord', 'setLoggerClass', 'shutdown',
           'warn', 'warning', 'getLogRecordFactory', 'setLogRecordFactory',
           'lastResort', 'raiseExceptions',
           ]

from logging_extended.git_handler import GitHandler
from datetime import datetime

VERBOSE = 5
TRACK = 25
CONFIG = 56

_additionalNameToLevel = {
    'VERBOSE': VERBOSE,
    'TRACK': TRACK,
    'CONFIG': CONFIG,
}
max_total_length = 90
min_number_of_spaces = 3

_useDefaultConfig = True

_gitConfig = {
    'auto_commit': False,
    'commit_message': "..."
}


class EnhancedLogger(Logger):
    def __init__(self, name, level=NOTSET):
        """
        Initialize the logger with a name and an optional level.
        """
        Logger.__init__(self, name, level)
        # Add new loglevels
        for key, val in _additionalNameToLevel.items():
            addLevelName(val, key)
        self._default_decorator = "#"
        # Set default config if applicable
        if _useDefaultConfig:
            _set_default_config()

    def _decorate_msg(self, msg, decorated, decorator=None):
        """
        Create a visual break, i.e. some kind of headline
        :param decorator: character that is used multiple times to make headline obvious
        :param msg: content of the headline. Maximum number of characters = 40
        :return:
        """
        if decorated:
            if decorator is None:
                decorator = self._default_decorator
            len_decorators = self._get_length_of_decorators(msg, decorator)
            if msg == "":
                msg = len_decorators * decorator
            else:
                msg = len_decorators * decorator + min_number_of_spaces * ' ' + msg \
                      + min_number_of_spaces * ' ' + len_decorators * decorator
        return msg

    @staticmethod
    def _get_length_of_decorators(msg, decorator):
        delimiter_length = len(decorator)
        if msg == '':
            num_delimiters = max_total_length
        else:
            num_delimiters = int((max_total_length - len(msg) - 2 * min_number_of_spaces)
                                 / (2 * delimiter_length))
        return num_delimiters

    def loop_counter(self, msg, count, level=INFO, decorator=None, max_loop_count=999):
        if self.isEnabledFor(level):
            max_loop_count = str(max_loop_count)
            count = str(count)
            count = (len(max_loop_count) - len(count)) * '0' + count
            print_str = msg + ' loop #' + count
            self._log(level, self._decorate_msg(print_str, True, decorator), tuple())

    def verbose(self, msg, decorated=False, decorator=None, *args, **kwargs):
        if self.isEnabledFor(VERBOSE):
            self._log(VERBOSE, self._decorate_msg(msg, decorated, decorator), args, **kwargs)

    def debug(self, msg, decorated=False, decorator=None, *args, **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "thorny problem", exc_info=1)
        """
        if self.isEnabledFor(DEBUG):
            self._log(DEBUG, self._decorate_msg(msg, decorated, decorator), args, **kwargs)

    def info(self, msg, decorated=False, decorator=None, *args, **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "interesting problem", exc_info=1)
        """
        if self.isEnabledFor(INFO):
            self._log(INFO, self._decorate_msg(msg, decorated, decorator), args, **kwargs)

    def track(self, msg, decorated=False, decorator=None, *args, **kwargs):
        if self.isEnabledFor(TRACK):
            self._log(TRACK, self._decorate_msg(msg, decorated, decorator), args, **kwargs)

    def warning(self, msg, decorated=False, decorator=None, *args, **kwargs):
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", "bit of a problem", exc_info=1)
        """
        if self.isEnabledFor(WARNING):
            self._log(WARNING, self._decorate_msg(msg, decorated, decorator), args, **kwargs)

    def error(self, msg, decorated=False, decorator=None, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "major problem", exc_info=1)
        """
        if self.isEnabledFor(ERROR):
            self._log(ERROR, self._decorate_msg(msg, decorated, decorator), args, **kwargs)

    def critical(self, msg, decorated=False, decorator=None, *args, **kwargs):
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=1)
        """
        if self.isEnabledFor(CRITICAL):
            self._log(CRITICAL, self._decorate_msg(msg, decorated, decorator), args, **kwargs)

    def config(self, msg, decorated=False, decorator=None, *args, **kwargs):
        if self.isEnabledFor(CONFIG):
            self._log(CONFIG, self._decorate_msg(msg, decorated, decorator), args, **kwargs)


setLoggerClass(EnhancedLogger)
_configRetriever = GitHandler()  # get git and other config


def getLogger(name=None) -> EnhancedLogger:
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    if name:
        return Logger.manager.getLogger(name)
    else:
        return root


def setGitConfig(config: dict):
    """
    Overwrite the git config to automatically commit on run
    :param config: dictionary with "git_commit_cwd: bool" and "git_commit_message"
    """
    global _gitConfig
    for key, val in config.items():
        if key in _gitConfig.keys():
            _gitConfig[key] = val
        else:
            raise ValueError(f"Unknown Git config key {key}")
    _configRetriever.update_config(_gitConfig)


def _print_project_info(logger):
    def log_config(msg):
        logger._log(CONFIG, msg, tuple())

    log_config('#' * max_total_length)
    log_config(f"Started run at {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
    msgs = _configRetriever.get_project_information()
    for msg in msgs:
        log_config(msg)
    log_config('#' * max_total_length)
    log_config('\n')


_print_project_info(Logger.manager.root)


def _set_default_config():
    import os
    global _useDefaultConfig

    logger = Logger.manager.root
    try:
        if logger.level == WARNING and (len(logger.handlers) == 0 or logger.handlers[0].formatter.datefmt is None):
            path_base = os.sep.join(os.path.abspath(__file__).split(os.sep)[:-1])
            path_config = os.path.join(path_base, "logging_config_console.ini")
            config.fileConfig(path_config)  # apply default config after start
    except Exception as e:
        logger.warning(f"Failed setting default formatting! {e}")
    _useDefaultConfig = False
