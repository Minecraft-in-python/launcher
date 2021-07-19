#!/usr/bin/env python3

from json import dump, load
from os import environ, mkdir, path, system
from shutil import copytree, rmtree
from sys import argv, executable, platform

def install():
    MCPYPATH = search_mcpy()
    if not path.isdir(MCPYPATH):
        mkdir(MCPYPATH)
    if '--skip-install-requirements' not in argv:
        print('[Install requirements]')
        pip = executable + ' -m pip'
        if '--hide-output' in argv:
            code = system('%s install -U -r %s >> %s' % (pip, get_file('requirements.txt'), path.devnull))
        else:
            code = system('%s install -U -r %s' % (pip, get_file('requirements.txt')))
        if code != 0:
            print('pip raise error code: %d' % code)
            exit(1)
        else:
            print('install successfully')
    print('[Copy lib]')
    if not path.isdir(path.join(MCPYPATH, 'launcher')):
        mkdir(path.join(MCPYPATH, 'launcher'))
    if not path.isdir(path.join(MCPYPATH, 'launcher', '.cache')):
        mkdir(path.join(MCPYPATH, 'launcher', '.cache'))
    install_settings()
    if not path.isdir(path.join(MCPYPATH, 'game')):
        mkdir(path.join(MCPYPATH, 'game')) 
    print('[Done]')

def get_file(f):
    # 返回文件目录下的文件名
    return path.abspath(path.join(path.dirname(__file__), f))

def install_settings():
    MCPYPATH = search_mcpy()
    source = {
            'check-deps': True,
            'lang': 'en_us',
            'version-list': 'https://minecraft-in-python.github.io/source/json/versions.json'
        }
    target = {}
    if path.isfile(path.join(MCPYPATH, 'launcher', 'settings.json')):
        target = load(open(path.join(MCPYPATH, 'launcher', 'settings.json')))
    for k, v in source.items():
        if (k not in target) or (not isinstance(k, type(v))):
            target[k] = v
    dump(target, open(path.join(MCPYPATH, 'launcher', 'settings.json'), 'w+'))

def search_mcpy():
    # 搜索文件存储位置
    if 'MCPYPATH' in environ:
        MCPYPATH = environ['MCPYPATH']
    elif platform == 'darwin':
        MCPYPATH = path.join(path.expanduser('~'), 'Library', 'Application Support', 'mcpy')
    elif platform.startswith('win'):
        MCPYPATH = path.join(path.expanduser('~'), 'mcpy')
    else:
        MCPYPATH = path.join(path.expanduser('~'), '.mcpy')
    return MCPYPATH

if __name__ == '__main__':
    install()
