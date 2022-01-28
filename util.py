import subprocess
import os
import logger
import time
from sys import platform
from win32com.client import Dispatch

TYPE_LINUX = 0
TYPE_MACOS = 1
TYPE_WINDOWS = 2

os_type = None


def is_revssh_running():
    path = get_home_folder() + "/start.revssh"
    if os.path.exists(path):
        f = open(path, "r")
        output = f.read().replace("\n", "").replace("\r", "")
        f.close()
        if not output or float(output) < (time.time() - 11 * 60):
            return False
        else:
            return True
    else:
        return False


def get_os_type():
    global os_type
    if os_type is None:
        if platform == "linux" or platform == "linux2":
            os_type = TYPE_LINUX
        elif platform == "darwin":
            os_type = TYPE_MACOS
        elif platform == "win32":
            os_type = TYPE_WINDOWS
    return os_type


def get_home_folder():
    if get_os_type() is TYPE_LINUX or get_os_type() is TYPE_LINUX:
        return "~"
    else:
        return "$HOME"


def get_username():
    output = subprocess.Popen("whoami", stdout=subprocess.PIPE)
    return str(output.communicate()[0]).replace("\n", "").replace("\r", "")


def get_hostname():
    return


def reboot():
    logger.info("Rebooting system")
    output = subprocess.Popen("reboot", stdout=subprocess.PIPE)
    return output.returncode == 0


def execute_command(command):
    output = subprocess.Popen(command, stdout=subprocess.PIPE)
    return output.communicate()[0].replace("\n", "").replace("\r", "")


def create_shortcut(path, target='', wdir='', icon=''):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wdir
    if icon == '':
        pass
    else:
        shortcut.IconLocation = icon
    shortcut.save()


def install_ssh():
    if get_os_type() == TYPE_WINDOWS:
        execute_command('powershell -command "& {&\'Get-WindowsCapability -Online | Where-Object Name -like '
                        '\'OpenSSH*\'\'}" ')
