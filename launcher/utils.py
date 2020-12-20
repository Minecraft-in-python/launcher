from os import environ, path
from sys import platform
import time

from colorama import Fore, Style, init

def log_err(text):
    # 打印错误信息
    print('%s[ERR  %s]%s %s' % (Fore.RED, time.strftime('%H:%M:%S'), Style.RESET_ALL, text))

def log_info(text):
    # 打印信息
    print('%s[INFO %s]%s %s' % (Fore.GREEN, time.strftime('%H:%M:%S'), Style.RESET_ALL, text))

def log_warn(text):
    # 打印警告信息
    print('%s[WARN %s]%s %s' % (Fore.YELLOW, time.strftime('%H:%M:%S'), Style.RESET_ALL, text))

def search_mcpy():
    # 搜索文件存储位置
    if 'MCPYPATH' in environ:
        MCPYPATH = environ['MCPYPATH']
    elif platform.startswith('win'):
        MCPYPATH = path.join(path.expanduser('~'), 'mcpy')
    else:
        MCPYPATH = path.join(path.expanduser('~'), '.mcpy')
    return MCPYPATH

init()
VERSION = {
        'major': 0,
        'minor': 1,
        'patch': 0,
        'str': '0.1'
        }
