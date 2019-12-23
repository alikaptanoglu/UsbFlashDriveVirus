__version__ = 1.0
__authors_names__ = 'Миненков & Гаврилов'

import winreg
import os
import subprocess
from shutil import rmtree, move
from uuid import uuid4


class MiGa(object):
    def __init__(self):
        self.PATH = 'C:\\Windows\\'
        self.VIRUS_NAME = 'dwrcs'
        self.VIRUS_IN_TASK_MANAGER = ['DRWCS.exe']
        self.VIRUS_IN_REGISTRY = ['Microsoft Windows Driver']
        self.viruses = self.find_viruses()

    def find_viruses(self):
        viruses = []
        for i in subprocess.getoutput("wmic process get description").split('\n\n'):
            new = i.replace(' ', '')
            if new.startswith('sys') and len(new) == 11 or new in self.VIRUS_IN_TASK_MANAGER \
                    or new.replace('.exe', '').isdigit():
                viruses.append(new)
        return viruses

    def kill_process(self):
        for i in range(len(self.viruses)):
            os.system(f'taskkill /f /im {i}')

    def delete_directory(self):
        try:
            rmtree(self.PATH + self.VIRUS_NAME)
        except FileNotFoundError:
            pass

        for i in os.listdir(self.PATH):
            if i.isdigit() or i == self.VIRUS_NAME:
                os.rename(self.PATH + i, str(uuid4()))

    def delete_in_register(self):
        a_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\Run\\", 0,
                               winreg.KEY_ALL_ACCESS)
        try:
            index = 0
            while True:
                nm = winreg.EnumValue(a_key, index)
                if self.PATH + self.VIRUS_NAME in nm[1] or nm[0] in self.VIRUS_IN_REGISTRY:
                    winreg.DeleteValue(a_key, nm[0])
                    print(nm)
                else:
                    index += 1
        except WindowsError:
            pass
        winreg.CloseKey(a_key)

    def delete_in_users(self):
        list_dir_name = 'C:\\Users\\' if os.path.isdir('C:\\Users\\') else 'C:\\Documents and Settings\\'
        list_dir = os.listdir(list_dir_name)
        for i in list_dir:
            try:
                if i == 'Default User':
                    continue
                list_dir_user = os.listdir(list_dir_name + i)
            except NotADirectoryError:
                continue
            for j in list_dir_user:
                if j.isdigit():
                    if os.listdir(list_dir_name + i + '\\' + j)[0] in self.viruses:
                        os.rename(list_dir_name + i + '\\' + j, str(uuid4()))

    def run(self):
        self.kill_process()
        self.delete_directory()
        self.delete_in_register()
        self.delete_in_users()


class ClearFlash(object):
    def __init__(self):
        pass

    @staticmethod
    def run(path):
        source = f'{path}:'
        dest = f'{path}:'
        files = os.listdir(source)
        try:
            os.system('attrib "*" -s -h -a -r /s /d')
            for f in files:
                if f == '__':
                    file = os.listdir(source + f)
                    for i in file:
                        if i.startswith('DriveM'):
                            os.remove(source + f + '\\' + i)
                        else:
                            move(source + f + '\\' + i, dest)
                    os.remove(f'{source}\\{f}')
        except FileNotFoundError:
            print('Не удается найти директорию')
        except PermissionError:
            pass


class ClearLink(object):
    def __init__(self):
        pass

    @staticmethod
    def run(path):
        os.chdir(f'{path}:')

        os.system('del /Q /F "\*.lnk"\n'
                  'attrib -s -h /d /s\n'
                  'for /d %%i in (\{*}) do rd %%i')


class Main:
    def __init__(self):
        self.clear_link = ClearLink()
        self.clear_flash = ClearFlash()
        self.miga = MiGa()

    def run(self):
        choise = None

        text = '___________________________________\n' \
               '\tГрафический интерфейс:\n' \
               '1. Удалить вирус флешки с пк.\n' \
               '2. Удалить вирус флешки на флешке.\n' \
               '3. Удалить вирус создающий ярлыки.\n' \
               '\t\tEnter - Выход.\n>: '

        while choise != '':
            choise = input(text)
            if choise == '1':
                self.run_miga()
            elif choise == '2':
                self.run_clear_flash()
            elif choise == '3':
                self.run_clear_link()
            else:
                print('Ну и куда ты жмёшь?\n'
                      'Я могу больше чем просто выключаться!')

    def run_clear_link(self):
        path = input('Введите букву диска.\n>:')
        self.clear_link.run(path)

    def run_clear_flash(self):
        path = input('Введите букву диска.\n>:')
        self.clear_flash.run(path)

    def run_miga(self):
        self.miga.run()


if __name__ == '__main__':
    print(f'Версия: {__version__}\n'
          f'Разрабы: {__authors_names__}\n\n')
    antivirus = Main()
    antivirus.run()
