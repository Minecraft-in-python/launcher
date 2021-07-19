from json import load
from os.path import abspath, dirname, isdir, isfile, join

from launcher.utils import *

path = {}
path['mcpypath'] = search_mcpy()
path['launcher'] = join(path['mcpypath'], 'launcher')
path['cache'] = join(path['launcher'], '.cache')
lang = dict()

settings = load(open(join(path['launcher'], 'settings.json'), encoding='utf-8'))
# 检查 settings.json 的正确性
for key in ['check-deps', 'lang', 'version-list']:
    if key not in settings:
        log_err("settings.json: missing '%s' key" % key)
        exit()
# lang 设置
if not isfile(abspath(join(dirname(__file__), 'assets', 'lang', settings['lang'] + '.json'))):
    log_err("settings.json: language '%s' not found" % settings['lang'])
    exit(1)

get_text = lambda s: lang[s] if s in lang else s

def set_lang():
    global lang
    lang = load(open(abspath(join(dirname(__file__), 'assets', 'lang', settings['lang'] + '.json')), encoding='utf-8'))

set_lang()
