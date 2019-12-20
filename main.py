import winreg
import os
import subprocess
from shutil import rmtree
from uuid import uuid4

PATH = 'C:\\Windows\\'
VIRUS_NAME = 'dwrcs'
VIRUS_IN_TASK_MANAGER = ['DRWCS.exe']
VIRUS_IN_REGISTRY = ['Microsoft Windows Driver']


def kill_process(virus_in_task_manager):
    for i in subprocess.getoutput("wmic process get description").split('\n\n'):
        new = i.replace(' ', '')
        if new.startswith('sys') and len(new) == 11 or new in virus_in_task_manager:
            os.system(f'taskkill /f /im {new}')


def delete_directory(path, virus_name):
    try:
        rmtree(path + virus_name)
    except FileNotFoundError:
        pass

    for i in os.listdir(path):
        if i.isdigit() or i == virus_name:
            os.rename(path + i, str(uuid4()))


def delete_on_register(path, virus_name, virus_in_registry):
    a_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\Run\\", 0,
                           winreg.KEY_ALL_ACCESS)
    try:
        for index in range(10000):
            nm = winreg.EnumValue(a_key, index)
            if path + virus_name in nm[1] or nm[0] in virus_in_registry:
                winreg.DeleteValue(a_key, nm[0])
    except WindowsError:
        pass
    winreg.CloseKey(a_key)


def delete_on_users():
    try:
        list_dir_name = 'C:\\Users\\'
        list_dir = os.listdir(list_dir_name)
    except FileNotFoundError:
        list_dir_name = 'C:\\Documents and Settings\\'
        list_dir = os.listdir(list_dir_name)

    for i in list_dir:
        try:
            list_dir_user = os.listdir(list_dir_name + i)
        except PermissionError:
            print('Запустите меня с правами администратора!')
            continue
        except NotADirectoryError:
            continue

        for j in list_dir_user:
            try:
                int(j)
                os.rename(list_dir_name + i + '\\' + j, str(uuid4()))
            except ValueError:
                continue


print('Разработчики:\n'
      'Миненков - vk.com/rym9n\n'
      'Гаврилов - vk.com/gavr17\n\n'
      'Version: 0.1.7\n')


if __name__ == '__main__':
    kill_process(VIRUS_IN_TASK_MANAGER)
    delete_on_register(PATH, VIRUS_NAME, VIRUS_IN_REGISTRY)
    delete_on_users()
    try:
        delete_directory(PATH, VIRUS_NAME)
    except PermissionError:
        print('Запустите программу от имени Администратора')

    input('Вирусы удалены.\n'
          'Нажмите "Enter".')
