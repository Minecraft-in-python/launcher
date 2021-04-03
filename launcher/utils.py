import os
from sys import platform
import time

_have_color = None
try:
    from colorama import Fore, Style, init
    init()
except ModuleNotFoundError:
    _have_color = False
else:
    _have_color = True

def log_err(text):
    # 打印错误信息
    if _have_color:
        print('%s[ERR  %s]%s %s' % (Fore.RED, time.strftime('%H:%M:%S'), Style.RESET_ALL, text))
    else:
        print('[ERR  %s] %s' % (time.strftime('%H:%M:%S'), text))

def log_info(text):
    # 打印信息
    if _have_color:
        print('%s[INFO %s]%s %s' % (Fore.GREEN, time.strftime('%H:%M:%S'), Style.RESET_ALL, text))
    else:
        print('[INFO %s] %s' % (time.strftime('%H:%M:%S'), text))

def log_warn(text):
    # 打印警告信息
    if _have_color:
        print('%s[WARN %s]%s %s' % (Fore.YELLOW, time.strftime('%H:%M:%S'), Style.RESET_ALL, text))
    else:
        print('[WARN %s] %s' % (time.strftime('%H:%M:%S'), text))

def search_mcpy():
    # 搜索文件存储位置
    if 'MCPYPATH' in os.environ:
        MCPYPATH = os.environ['MCPYPATH']
    elif platform == 'darwin':
        MCPYPATH = path.join(path.expanduser('~'), 'Library', 'Application Support', 'mcpy')
    elif platform.startswith('win'):
        MCPYPATH = os.path.join(os.path.expanduser('~'), 'mcpy')
    else:
        MCPYPATH = os.path.join(os.path.expanduser('~'), '.mcpy')
    return MCPYPATH

init()
VERSION = {
        'major': 0,
        'minor': 1,
        'patch': 0,
        'str': '0.1'
        }
