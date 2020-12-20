from io import DEFAULT_BUFFER_SIZE
from hashlib import sha256
import os
from threading import Thread
from tkinter import *
import tkinter.ttk as ttk

from launcher.source import get_lang, path
from launcher.utils import log_info

from requests import get


class InstallDialogue(Toplevel):

    def __init__(self, url, total):
        Toplevel.__init__(self)
        self.title(get_lang('launcher.dialogue.install.title'))
        self.resizable(False, False)
        self._widget = {}
        self._url = url
        self._total = total
        self.create_widget()
        self.pack_widget()
        self.download()

    def create_widget(self):
        self._widget['dialogue.label'] = ttk.Label(self, text='wait')

    def pack_widget(self):
        self._widget['dialogue.label'].grid(column=0, row=0, sticky='new')

    def download(self):
        try:
            log_info('download')
            result = get(self._url)
            log_info('done')
        except:
            pass
        if result.status_code != 200:
            log_info('err')
        else:
            sha = sha256()
            sha.update(self._url.encode())
            name = sha.hexdigest()[:7] + '.zip'
            with open(os.path.join(path['launcher'], '.cache', name), 'wb') as f:
                f.write(result.content)
            f.close()
            self.destroy()
