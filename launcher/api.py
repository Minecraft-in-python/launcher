from json import load, dump
import os
import re
from requests import get
import sys
import uuid

from launcher.source import path, settings
from launcher.utils import *

def get_lang_list():
    lang_dir = os.path.join(path['launcher'], 'lang')
    lang_list = []
    for f in os.listdir(lang_dir):
        with open(os.path.join(lang_dir, f)) as s:
            lang_list.append(load(s)['description'])
    else:
        return lang_list

def get_versions():
    result = get(settings['version-list'])
    if result.status_code != 200:
        log_err('version list not available')
        exit(1)
    else:
        return result.json()

def has_deps(deps):
    for d in sys.path:
        if os.path.isdir(d):
            for dep in deps:
                if dep in os.listdir(d):
                    deps.remove(dep)
    else:
        return deps

def has_register():
    if os.path.isfile(os.path.join(path['mcpypath'], 'player.json')):
        player = load(open(os.path.join(path['mcpypath'], 'player.json')))
        for key in ['id', 'name']:
            if key not in player:
                return False
        else:
            if not re.match(r'^([a-z]|[A-Z]|_)\w+$', player['name']):
                return False
            if not re.match('^[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}$', player['id']):
                return False
            return True
    else:
        return False

def get_name():
    if has_register():
        return load(open(os.path.join(path['mcpypath'], 'player.json')))['name']
    else:
        return ''

def register(name):
    player = {}
    player['id'] = str(uuid.uuid4())
    player['name'] = name
    dump(player, open(os.path.join(path['mcpypath'], 'player.json'), 'w+'), indent='\t')

def rename(name):
    player = load(open(os.path.join(path['mcpypath'], 'player.json')))
    player['name'] = name
    dump(player, open(os.path.join(path['mcpypath'], 'player.json'), 'w+'), indent='\t')
