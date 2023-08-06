import logging
import traceback
import sys
import os
import platform
import inspect

stack_t = inspect.stack()
ins = inspect.getframeinfo(stack_t[1][0])
file_dir = os.path.dirname(os.path.abspath(ins.filename))
log_dir = os.path.join(file_dir, "logs")
if os.path.exists(log_dir) is False:
    os.mkdir(log_dir)

log_path=os.path.join(file_dir, "logs",  "fxtext_debug.log")
header="FXTEST"
_logger = logging.getLogger('fxtest')
_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_path, encoding="utf-8")
steram_handler = logging.StreamHandler()

Log_Format="{header} [%(asctime)s] [%(name)s] [%(levelname)s] [%(lineno)d] %(message)s".format(header=header)
formatter=logging.Formatter(
    fmt=Log_Format,
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
steram_handler.setFormatter(formatter)


if platform.system().lower() == "windows":
    _logger.addHandler(file_handler)
    _logger.addHandler(steram_handler)
    
else:
    _logger.addHandler(file_handler)
    _logger.addHandler(steram_handler)
    _logger.removeHandler(steram_handler)


def debug(msg):
    # _logger.debug(now + " [DEBUG] " + str(msg))
    _logger.debug(msg)


def info(msg):
    
    # _logger.info(Fore.GREEN + now + " [INFO] " + str(msg) + Style.RESET_ALL)
    _logger.info(msg)

def error(msg):
    # _logger.error(Fore.RED + now + " [ERROR] " + str(msg) + Style.RESET_ALL)
    _logger.error(msg)

def warn(msg):
    # _logger.warning(Fore.YELLOW + now + " [WARNING] " + str(msg) + Style.RESET_ALL)
    _logger.warning(msg)
    

def _print(msg):
    # _logger.debug(Fore.BLUE + now + " [PRINT] " + str(msg) + Style.RESET_ALL)
    _logger.debug(msg)

def set_level(level):
    """ 设置log级别

    :param level: logging.DEBUG, logging.INFO, logging.WARN, logging.ERROR
    :return:
    """
    _logger.setLevel(level)


def set_level_to_debug():
    _logger.setLevel(logging.DEBUG)


def set_level_to_info():
    _logger.setLevel(logging.INFO)


def set_level_to_warn():
    _logger.setLevel(logging.WARN)


def set_level_to_error():
    _logger.setLevel(logging.ERROR)
