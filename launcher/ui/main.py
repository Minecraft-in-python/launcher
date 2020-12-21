from hashlib import sha256
from io import DEFAULT_BUFFER_SIZE
import os
import subprocess
from sys import executable, platform
from threading import Thread
from tkinter import *
import tkinter.ttk as ttk
from zipfile import ZipFile

from launcher import api
from launcher.source import get_lang, path
from launcher.utils import *

from requests import get


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
        self._widget['main.start.start'] = ttk.Button(self._widget['main.start'],
                text=get_lang('launcher.main.start.start'), command=self.start_game)
        # notebook 之 install
        self._widget['main.install.refresh'] = ttk.Button(self._widget['main.install'],
                text=get_lang('launcher.main.install.refresh'), command=self.set_versions)
        self._widget['main.install.select_site'] = ttk.Combobox(self._widget['main.install'], width=10)
        self._widget['main.install.select_site'].set('github')
        self._widget['main.install.select_site'].state(['readonly'])
        self._widget['main.install.version_list'] = Listbox(self._widget['main.install'], height=10)
        self.set_versions()
        self._widget['main.install.scrollbar'] = ttk.Scrollbar(self._widget['main.install'],
                command=self._widget['main.install.version_list'].yview)
        self._widget['main.install.version_list'].configure(yscrollcommand=self._widget['main.install.scrollbar'].set)
        self._widget['main.install.install'] = ttk.Button(self._widget['main.install'],
                text=get_lang('launcher.main.install.install'), command=self.install_version)
        self._widget['main.install.uninstall'] = ttk.Button(self._widget['main.install'],
                text=get_lang('launcher.main.install.uninstall'))
        self._widget['main.install.status'] = ttk.Label(self._widget['main.install'],
                text=get_lang('launcher.main.install.status')[0])
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
        self._widget['main.install.select_site'].grid(column=1, row=0, pady=2, sticky='ne')
        self._widget['main.install.version_list'].grid(column=0, columnspan=2, row=1, sticky='news')
        self._widget['main.install.scrollbar'].grid(column=2, row=1, sticky='nes')
        self._widget['main.install.install'].grid(column=0, row=2, sticky='ws')
        self._widget['main.install.uninstall'].grid(column=1, row=2, sticky='ws')
        self._widget['main.install.status'].grid(column=0, columnspan=2, row=3, padx=3, pady=3)
        self._widget['main.settings.version'].grid(column=0, columnspan=2, row=0, sticky='nw')
        self._widget['main.settings.language_label'].grid(column=0, row=1, pady=3, sticky='nw')
        self._widget['main.settings.language'].grid(column=1, row=1, sticky='nw')
        self.resizable(False, False)

    def download(self, version, url, total):
        sha = sha256()
        sha.update(url.encode())
        name = os.path.join(path['launcher'], '.cache', sha.hexdigest()[:7] + '.zip')
        result = get(url, stream=True)
        if result.status_code != 200:
            self._widget['main.install.status'].configure(text=get_lang('launcher.main.install.status')[3])
            return
        size = 0
        self._widget['main.install.status'].configure(text=get_lang('launcher.main.install.status')[1] % 0)
        with open(name, 'wb') as f:
            for chunk in result.iter_content(DEFAULT_BUFFER_SIZE):
                size += int(len(chunk))
                self._widget['main.install.status'].configure(
                        text=get_lang('launcher.main.install.status')[1] % int(size / total * 100))
                f.write(chunk)
        f.close()
        self._widget['main.install.status'].configure(text=get_lang('launcher.main.install.status')[2])
        ZipFile(name).extractall(os.path.join(path['mcpypath'], 'game', version))
        ret = subprocess.run([
            executable,
            os.path.join(path['mcpypath'], 'game', version, 'Minecraft', 'install.py'),
            '--no-install-requirements', '--no-register'
        ], capture_output=True)
        if ret.returncode != 0:
            self._widget['main.install.status'].configure(text=get_lang('launcher.main.install.status')[3])
        else:
            self._widget['main.install.status'].configure(text=get_lang('launcher.main.install.status')[0])

    def install_version(self):
        select = self._widget['main.install.version_list'].curselection()
        if select == ():
            log_warn('no version selected')
            return
        site = self._widget['main.install.select_site'].get()
        version = self._widget['main.install.version_list'].get(select[0])
        if version[0] == '*':
            version = version[1:]
        for ver in self._versions:
            if ver['version'] == version:
                Thread(target=self.download, args=(version, ver['url'][site], ver['bytes'])).start()
                break

    def set_language(self):
        lang = tuple(api.get_lang_list())
        self._widget['main.settings.language']['values'] = lang

    def set_versions(self, events=None):
        self._versions = api.get_versions()
        self._widget['main.install.version_list'].delete(0, 'end')
        self._widget['main.install.select_site'].configure(values=list(self._versions[0]['url'].keys()))
        self._widget['main.install.select_site'].set(list(self._versions[0]['url'].keys())[0])
        versions = []
        installed = []
        for version in self._versions:
            if version['version'] in os.listdir(os.path.join(path['mcpypath'], 'game')):
                self._widget['main.install.version_list'].insert('end', '*' + version['version'])
                installed.append(version['version'])
            else:
                self._widget['main.install.version_list'].insert('end', version['version'])
        else:
            self._widget['main.start.select_version'].configure(values=installed)

    def start_game(self):
        version = self._widget['main.start.select_version'].get()
        if version in os.listdir(os.path.join(path['mcpypath'], 'game')):
            os.chdir(os.path.join(path['mcpypath'], 'game', version, 'Minecraft'))
            subprocess.run([executable, '-m', 'Minecraft'])
