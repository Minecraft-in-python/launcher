from hashlib import sha256
from io import DEFAULT_BUFFER_SIZE
import os
import re
import subprocess
from shutil import move, rmtree
from sys import executable, platform
import time
from threading import Thread
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from zipfile import ZipFile

from launcher import api
from launcher.source import get_text, path, settings
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
        self.title(get_text('launcher.main.title'))
        self._widget = {}
        self._var = {}
        if not platform.startswith('win'):
            theme = os.path.dirname(os.path.abspath(__file__)) + '/theme/arc'
            self.tk.eval('lappend auto_path {%s}' % theme)
            ttk.Style().theme_use('arc')
        self._versions = api.get_versions()
        self.create_widget()
        self.pack_widget()
        deps = api.has_deps(['pyglet', 'psutil', 'opensimplex'])

    def create_widget(self):
        # notebook 部件
        self._widget['main'] = ttk.Notebook(self)
        self._widget['main.start'] = ttk.Frame(self._widget['main'])
        self._widget['main.install'] = ttk.Frame(self._widget['main'])
        self._widget['main.settings'] = ttk.Frame(self._widget['main'])
        self._widget['main'].add(self._widget['main.start'], text=get_text('launcher.main.start.title'))
        self._widget['main'].add(self._widget['main.install'], text=get_text('launcher.main.install.title'))
        self._widget['main'].add(self._widget['main.settings'], text=get_text('launcher.main.settings.title'))
        # notebook 之 start
        self._widget['main.start.select_version'] = ttk.Combobox(self._widget['main.start'], width=10)
        self._widget['main.start.select_version'].state(['readonly'])
        self._widget['main.start.start'] = ttk.Button(self._widget['main.start'],
                text=get_text('launcher.main.start.start'), command=self.start_game)
        self._widget['main.start.sep'] = ttk.Separator(self._widget['main.start'], orient='horizontal')
        self._widget['main.start.name'] = ttk.Entry(self._widget['main.start'], width=12,
                validate='key', validatecommand=(self.register(self.test_name), '%P'))
        self._widget['main.start.manage'] = ttk.Button(self._widget['main.start'],
                text=get_text('launcher.main.start.manage')['register' if not api.has_register() else 'rename'],
                command=self.manage_player)
        self._widget['main.start.name'].delete(0, 'end')
        self._widget['main.start.name'].insert(0, api.get_name())
        # notebook 之 install
        self._widget['main.install.refresh'] = ttk.Button(self._widget['main.install'],
                text=get_text('launcher.main.install.refresh'), command=self.refresh)
        self._widget['main.install.select_site'] = ttk.Combobox(self._widget['main.install'], width=10)
        self._widget['main.install.select_site'].set('github')
        self._widget['main.install.select_site'].state(['readonly'])
        self._widget['main.install.version_list'] = Listbox(self._widget['main.install'], height=10)
        self.set_versions()
        self._widget['main.install.scrollbar'] = ttk.Scrollbar(self._widget['main.install'],
                command=self._widget['main.install.version_list'].yview)
        self._widget['main.install.version_list'].configure(yscrollcommand=self._widget['main.install.scrollbar'].set)
        self._widget['main.install.install'] = ttk.Button(self._widget['main.install'],
                text=get_text('launcher.main.install.install'), command=self.install_version)
        self._widget['main.install.uninstall'] = ttk.Button(self._widget['main.install'],
                text=get_text('launcher.main.install.uninstall'), command=self.uninstall_version)
        self._widget['main.install.status'] = ttk.Label(self._widget['main.install'],
                text=get_text('launcher.main.install.status')[0])
        # notebook 之 settings
        self._widget['main.settings.version'] = ttk.Label(self._widget['main.settings'],
                text=get_text('launcher.main.settings.text')[0] % VERSION['str'])
        self._widget['main.settings.language_label'] = ttk.Label(self._widget['main.settings'],
                text=get_text('launcher.main.settings.language'))
        self._widget['main.settings.language'] = ttk.Combobox(self._widget['main.settings'],
                text=get_text('launcher.main.settings.language'), width=15)
        self._widget['main.settings.language'].state(['readonly'])
        self.set_language()
        self._widget['main.settings.clean_cache'] = ttk.Button(self._widget['main.settings'],
                text=get_text('launcher.main.settings.clean_cache'), command=self.clean_cache)
        self._widget['main.settings.credits'] = ttk.Label(self._widget['main.settings'],
                text=get_text('launcher.main.settings.text')[1], justify='right')

    def pack_widget(self):
        self._widget['main'].grid(column=0, row=0, padx=5, pady=5, sticky='news')
        self._widget['main.start.select_version'].grid(column=0, row=0, padx=3, pady=3, sticky='es')
        self._widget['main.start.start'].grid(column=1, row=0, sticky='es')
        self._widget['main.start.sep'].grid(column=0, columnspan=2, row=1, padx=5, pady=5, sticky='we')
        self._widget['main.start.name'].grid(column=0, row=2, padx=3, pady=3, sticky='nw')
        self._widget['main.start.manage'].grid(column=1, row=2, sticky='nw')
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
        self._widget['main.settings.clean_cache'].grid(column=0, columnspan=2, row=2, sticky='nw')
        self._widget['main.settings.credits'].grid(column=0, columnspan=2, row=3, sticky='es')
        self.resizable(False, False)

    def clean_cache(self):
        rmtree(path['cache'])
        os.mkdir(path['cache'])

    def download(self, version, url, hash_, total):
        sha_name, sha_check = sha256(), sha256()
        sha_name.update(url.encode())
        name = os.path.join(path['cache'], sha_name.hexdigest()[:7] + '.zip')
        if not os.path.isfile(name):
            result = get(url, stream=True)
            if result.status_code != 200:
                self._widget['main.install.status'].configure(text=get_text('launcher.main.install.status')[3])
                return
            size = 0
            self._widget['main.install.status'].configure(text=get_text('launcher.main.install.status')[1] % 0)
            with open(name, 'wb') as f:
                for chunk in result.iter_content(DEFAULT_BUFFER_SIZE):
                    size += int(len(chunk))
                    self._widget['main.install.status'].configure(
                            text=get_text('launcher.main.install.status')[1] % int(size / total * 100))
                    f.write(chunk)
            f.close()
            sha_check.update(open(name, 'rb').read())
            if sha_check.hexdigest()[:7] != hash_:
                log_info('Hash not same')
                self._widget['main.install.status'].configure(text=get_text('launcher.main.install.status')[3])
                return
            self._widget['main.install.status'].configure(text=get_text('launcher.main.install.status')[2])
        zf = ZipFile(name)
        zf.extractall(os.path.join(path['mcpypath'], 'game', version))
        ret = subprocess.run([
            executable,
            os.path.join(path['mcpypath'], 'game', version, 'Minecraft', 'install.py'),
            '--no-install-requirements', '--skip-register'
        ], capture_output=False)
        if ret.returncode != 0:
            log_info('Install error')
            self._widget['main.install.status'].configure(text=get_text('launcher.main.install.status')[3])
        else:
            self._widget['main.install.status'].configure(text=get_text('launcher.main.install.status')[0])
        self.set_versions()

    def install_version(self):
        select = self._widget['main.install.version_list'].curselection()
        if select == ():
            log_warn('no version selected')
            return
        site = self._widget['main.install.select_site'].get()
        version = self._widget['main.install.version_list'].get(select[0])
        if version[0] == '*':
            version = version[1:]
        for ver in self._versions['resource']:
            if ver['version'] == version:
                site = self._versions['site'][site] % ver['url'][site]
                Thread(target=self.download, args=(version, site, ver['hash'], ver['bytes'])).start()
                break

    def uninstall_version(self):
        select = self._widget['main.install.version_list'].curselection()
        if select == ():
            log_warn('no version selected')
            return
        version = self._widget['main.install.version_list'].get(select[0])
        if version[0] == '*':
            if version[1:] in os.listdir(os.path.join(path['mcpypath'], 'game')):
                if messagebox.askyesno(title=get_text('launcher.main.install.uninstall.message')['title'],
                        message=get_text('launcher.main.install.uninstall.message')['message'] % version[1:]):
                    rmtree(os.path.join(path['mcpypath'], 'game', version[1:]))
                    self.set_versions()

    def set_language(self):
        lang = tuple(api.get_lang_list())
        self._widget['main.settings.language']['values'] = lang

    def refresh(self):
        self._versions = api.get_versions()
        self.set_versions()

    def set_versions(self):
        self._widget['main.install.version_list'].delete(0, 'end')
        self._widget['main.install.select_site'].configure(values=list(self._versions['site'].keys()))
        self._widget['main.install.select_site'].set(list(self._versions['site'].keys())[0])
        versions = []
        installed = []
        for version in self._versions['resource']:
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
            if settings['check-deps']:
                deps = []
                for line in open('requirements.txt', 'r+').readlines():
                    if line.rindex('=') == -1:
                        deps.append(line.strip())
                    else:
                        deps.append(line[:line.rindex('=') - 1])
                else:
                    deps = api.has_deps(deps)
                    if deps:
                        messagebox.showinfo(message=get_text('launcher.main.start.missing_deps') % ', '.join(deps))
            self.iconify()
            subprocess.run([executable, '-m', 'Minecraft'])
            self.deiconify()

    def test_name(self, s):
        valid = re.match(r'^([a-z]|[A-Z]|_)\w+$', s) is not None
        self._widget['main.start.manage'].state(['!disabled'] if valid else ['disabled'])
        if len(s) <= 2:
            return True
        else:
            return valid

    def manage_player(self):
        if api.has_register():
            api.rename(self._widget['main.start.name'].get())
        else:
            api.register(self._widget['main.start.name'].get())
            self._widget['main.start.manage'].configure(text=get_text('launcher.main.start.manage')['rename'])
