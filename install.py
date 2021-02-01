#!/usr/bin/env python3

from json import dump, load
from os import environ, mkdir, path, system
from shutil import copytree, rmtree
from sys import argv, executable, platform

def install():
    MCPYPATH = search_mcpy()
    if not path.isdir(MCPYPATH):
        mkdir(MCPYPATH)
    if '--no-install-requirements' not in argv:
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
    install_json('settings.json')
    if path.isdir(path.join(MCPYPATH, 'launcher', 'lang')):
        rmtree(path.join(MCPYPATH, 'launcher', 'lang'))
    copytree(path.join(get_file('data'), 'lang'), path.join(MCPYPATH, 'launcher', 'lang'))
    if path.isdir(path.join(MCPYPATH, 'launcher', 'texture')):
        rmtree(path.join(MCPYPATH, 'launcher', 'texture'))
    # copytree(path.join(get_file('data'), 'texture'), path.join(MCPYPATH, 'launcher', 'texture'))
    if not path.isdir(path.join(MCPYPATH, 'game')):
        mkdir(path.join(MCPYPATH, 'game')) 
    print('[Done]')

def get_file(f):
    # 返回文件目录下的文件名
    return path.abspath(path.join(path.dirname(__file__), f))

def install_json(f):
    MCPYPATH = search_mcpy()
    source = load(open(path.join(get_file('data'), f)))
    target = {}
    if path.isfile(path.join(MCPYPATH, 'launcher', f)):
        target = load(open(path.join(MCPYPATH, 'launcher', f)))
    else:
        target = {}
    for k, v in source.items():
        if k not in target:
            target[k] = v
    dump(target, open(path.join(MCPYPATH, 'launcher', f), 'w+'))

def search_mcpy():
    # 搜索文件存储位置
    if 'MCPYPATH' in environ:
        MCPYPATH = environ['MCPYPATH']
    elif platform.startswith('win'):
        MCPYPATH = path.join(path.expanduser('~'), 'mcpy')
    else:
        MCPYPATH = path.join(path.expanduser('~'), '.mcpy')
    return MCPYPATH

if __name__ == '__main__':
    install()
