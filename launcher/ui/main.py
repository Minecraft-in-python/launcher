import os
from tkinter import *
import tkinter.ttk as ttk

from launcher import api
from launcher.source import get_lang
from launcher.utils import *


class MinecraftLauncher(Tk):

    def __init__(self):
        try:
            Tk.__init__(self)
        except:
            log_err('no display, exit')
            exit(1)
        log_info('Minecraft launcher %s' % VERSION['str'])
        self.title(get_lang('launcher.main.title'))
        self._widget = {}
        self._var = {}
        theme = os.path.dirname(os.path.abspath(__file__)) + '/../theme/arc'
        self.tk.eval('lappend auto_path {%s}' % theme)
        ttk.Style().theme_use('arc')
        self.create_var()
        self.create_widget()
        self.pack_widget()

    def create_widget(self):
        # notebook 部件
        self._widget['main'] = ttk.Notebook(self)
        self._widget['main.start'] = ttk.Frame(self._widget['main'])
        self._widget['main.install'] = ttk.Frame(self._widget['main'])
        self._widget['main.settings'] = ttk.Frame(self._widget['main'])
        self._widget['main'].add(self._widget['main.start'], text=get_lang('launcher.main.start.title'))
        self._widget['main'].add(self._widget['main.install'], text=get_lang('launcher.main.install.title'))
        self._widget['main'].add(self._widget['main.settings'], text=get_lang('launcher.main.settings.title'))
        # notebook 之 start
        self._widget['main.start.select_version'] = ttk.Combobox(self._widget['main.start'],
                textvariable=self._var['start.select_version'], width=10)
        self._widget['main.start.select_version'].state(['readonly'])
        self._widget['main.start.start'] = ttk.Button(self._widget['main.start'], text=get_lang('launcher.main.start.start'))
        # notebook 之 install
        self._widget['main.install.version_list'] = Listbox(self._widget['main.install'], height=10)
        self.set_versions()
        self._widget['main.install.scrollbar'] = ttk.Scrollbar(self._widget['main.install'],
                command=self._widget['main.install.version_list'].yview)
        self._widget['main.install.version_list'].configure(yscrollcommand=self._widget['main.install.scrollbar'].set)
        # self.resizable(False, False)

    def create_var(self):
        self._var['start.select_version'] = StringVar()

    def pack_widget(self):
        self._widget['main'].grid(column=0, row=0, padx=5, pady=5, sticky='news')
        self._widget['main.start.select_version'].grid(column=0, row=0, pady=5, sticky='es')
        self._widget['main.start.start'].grid(column=0, row=1, sticky='es')
        self._widget['main.install.version_list'].grid(column=0, columnspan=2, row=0, sticky='news')
        self._widget['main.install.scrollbar'].grid(column=2, row=0, sticky='nes')

    def set_versions(self):
        self._widget['main.install.version_list'].delete(0, 'end')
        json = api.get_versions()
        versions = []
        for item in json:
            self._widget['main.install.version_list'].insert('end', item['version'])
