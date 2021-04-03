#!/usr/bin/env python3

import os
import subprocess
from sys import argv, executable, platform

def search_mcpy():
    # 搜索文件存储位置
    if 'MCPYPATH' in os.environ:
        MCPYPATH = environ['MCPYPATH']
    elif platform == 'darwin':
        MCPYPATH = path.join(path.expanduser('~'), 'Library', 'Application Support', 'mcpy')
    elif platform.startswith('win'):
        MCPYPATH = os.path.join(os.path.expanduser('~'), 'mcpy')
    else:
        MCPYPATH = os.path.join(os.path.expanduser('~'), '.mcpy')
    return MCPYPATH

def main():
    if len(argv) < 2:
        print('arguments not enough')
        return
    if argv[1] == 'run':
        if len(argv) == 3:
            run(argv[2])
        else:
            print("subcommand 'run' takes 2 arguments, but %d found" % (len(argv) - 1))
    elif argv[1] == 'list':
        list_()
    else:
        print("subcommand '%s' not found" % argv[1])

def run(version):
    if os.path.isdir(os.path.join(search_mcpy(), 'game', version, 'Minecraft')):
        print('start version %s' % version)
        os.chdir(os.path.join(search_mcpy(), 'game', version, 'Minecraft'))
        subprocess.run([executable, '-m', 'Minecraft'])
    else:
        print("version '%s' not found" % version)

def list_():
    print('available versions:')
    for f in os.listdir(os.path.join(search_mcpy(), 'game')):
        print(' - %s' % f)

if __name__ == '__main__':
    main()
