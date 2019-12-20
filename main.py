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
    viruses = []
    for i in subprocess.getoutput("wmic process get description").split('\n\n'):
        new = i.replace(' ', '')
        if new.startswith('sys') and len(new) == 11 or new in virus_in_task_manager or new.replace('.exe', '').isdigit():
            os.system(f'taskkill /f /im {new}')
            viruses.append(new)
    return viruses
        


def delete_directory(path, virus_name):
    try:
        rmtree(path + virus_name)
    except FileNotFoundError:
        pass

    for i in os.listdir(path):
        if i.isdigit() or i == virus_name:
            os.rename(path + i, str(uuid4()))


def delete_in_register(path, virus_name, virus_in_registry):
    a_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\Run\\", 0,
                           winreg.KEY_ALL_ACCESS)
    try:
        index = 0
        while True:
            nm = winreg.EnumValue(a_key, index)
            if path + virus_name in nm[1] or nm[0] in virus_in_registry:
                winreg.DeleteValue(a_key, nm[0])
            index += 1
    except WindowsError:
        pass
    winreg.CloseKey(a_key)


def delete_in_users(viruses):
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
                if any(viruses) in os.listdir(list_dir_name + i + '\\' + j):
                    os.rename(list_dir_name + i + '\\' + j, str(uuid4()))


def main():
    try:
        delete_in_register(PATH, VIRUS_NAME, VIRUS_IN_REGISTRY)
        delete_in_users(kill_process(VIRUS_IN_TASK_MANAGER))
        delete_directory(PATH, VIRUS_NAME)
    except PermissionError:
        print('Запустите программу от имени Администратора')

    input('Вирусы удалены.\n'
          'Нажмите "Enter".')


print('Разработчики:\n'
      'Миненков - vk.com/rym9n\n'
      'Гаврилов - vk.com/gavr17\n\n'
      'Version: 0.1.10\n')


if __name__ == '__main__':
    main()
