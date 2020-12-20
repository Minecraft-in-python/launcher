import os
from sys import platform
from tkinter import *
import tkinter.ttk as ttk

from launcher import api
from launcher.source import get_lang
from launcher.ui.dialogue import InstallDialogue
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
        if not platform.startswith('win'):
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
        self._widget['main.install.refresh'] = ttk.Button(self._widget['main.install'],
                text=get_lang('launcher.main.install.refresh'), command=self.set_versions)
        self._widget['main.install.version_list'] = Listbox(self._widget['main.install'], height=10)
        self.set_versions()
        self._widget['main.install.scrollbar'] = ttk.Scrollbar(self._widget['main.install'],
                command=self._widget['main.install.version_list'].yview)
        self._widget['main.install.version_list'].configure(yscrollcommand=self._widget['main.install.scrollbar'].set)
        self._widget['main.install.install'] = ttk.Button(self._widget['main.install'],
                text=get_lang('launcher.main.install.install'), command=self.install_version)
        self._widget['main.install.uninstall'] = ttk.Button(self._widget['main.install'],
                text=get_lang('launcher.main.install.uninstall'))
        # notebook 之 settings
        self._widget['main.settings.version'] = ttk.Label(self._widget['main.settings'],
                text=get_lang('launcher.main.settings.text')[0] % VERSION['str'])
        self._widget['main.settings.language_label'] = ttk.Label(self._widget['main.settings'],
                text=get_lang('launcher.main.settings.language'))
        self._widget['main.settings.language'] = ttk.Combobox(self._widget['main.settings'],
                text=get_lang('launcher.main.settings.language'), width=10)
        self._widget['main.settings.language'].state(['readonly'])
        self.set_language()

    def create_var(self):
        self._var['start.select_version'] = StringVar()

    def pack_widget(self):
        self._widget['main'].grid(column=0, row=0, padx=5, pady=5, sticky='news')
        self._widget['main.start.select_version'].grid(column=0, row=0, pady=5, sticky='es')
        self._widget['main.start.start'].grid(column=0, row=1, sticky='es')
        self._widget['main.install.refresh'].grid(column=0, row=0, sticky='nw')
        self._widget['main.install.version_list'].grid(column=0, columnspan=2, row=1, sticky='news')
        self._widget['main.install.scrollbar'].grid(column=2, row=1, sticky='nes')
        self._widget['main.install.install'].grid(column=0, row=2, sticky='ws')
        self._widget['main.install.uninstall'].grid(column=1, row=2, sticky='ws')
        self._widget['main.settings.version'].grid(column=0, columnspan=2, row=0, sticky='nw')
        self._widget['main.settings.language_label'].grid(column=0, row=1, sticky='nw')
        self._widget['main.settings.language'].grid(column=1, row=1, sticky='nw')
        self.resizable(False, False)

    def install_version(self):
        select = self._widget['main.install.version_list'].curselection()
        if select == ():
            log_warn('no version selected')
            return
        version = self._widget['main.install.version_list'].get(select[0])
        for ver in self._versions:
            if ver['version'] == version:
                dialogue = InstallDialogue(ver['url']['gitee'], ver['bytes'])
                dialogue.mainloop()

    def set_language(self):
        lang = tuple(api.get_lang_list())
        self._widget['main.settings.language']['values'] = lang

    def set_versions(self, events=None):
        self._versions = api.get_versions()
        self._widget['main.install.version_list'].delete(0, 'end')
        versions = []
        for version in self._versions:
            self._widget['main.install.version_list'].insert('end', version['version'])
