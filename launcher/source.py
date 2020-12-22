from json import load
from os.path import isdir, isfile, join

from launcher.utils import *

path = {}
path['mcpypath'] = search_mcpy()
path['launcher'] = join(path['mcpypath'], 'launcher')

settings = load(open(join(path['launcher'], 'settings.json'), encoding='utf-8'))
# 检查 settings.json 的正确性
for key in ['lang', 'version-list']:
    if key not in settings:
        log_err("settings.json: missing '%s' key" % key)
        exit()
# lang 设置
if not isfile(join(path['launcher'], 'lang', settings['lang'] + '.json')):
    log_err("settings.json: language '%s' not found" % settings['lang'])
    exit(1)

lang = load(open(join(path['launcher'], 'lang', settings['lang'] + '.json'), encoding='utf-8'))
get_lang = lambda s: lang[s] if s in lang else s
