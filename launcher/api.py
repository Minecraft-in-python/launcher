from requests import get

from launcher.utils import *

def get_versions():
    result = get('https://Minecraft-in-python.github.io/json/versions.json')
    if result.status_code != 200:
        log_err('version list not available')
        return []
    else:
        return result.json()
