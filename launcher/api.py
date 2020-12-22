from json import load
import os
from requests import get

from launcher.source import path, settings
from launcher.utils import log_err

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
