import os
import subprocess
import logger
import util


def create_startup_crontab():
    os_type = util.get_os_type()
    if os_type is util.TYPE_LINUX or os_type == util.TYPE_MACOS:
        return create_crontab("*/10 * * * * python " + os.path.dirname(os.path.realpath(__file__)) + "/main.py") \
               and create_crontab("@reboot python " + os.path.dirname(os.path.realpath(__file__)) + "/main.py")
    else:
        startup_dir = util.get_home_folder() + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
        target = os.path.dirname(os.path.abspath(__file__))
        target = os.path.realpath(target)
        directory = target.rsplit('\\', 1)[0]
        util.create_shortcut(os.path.join(startup_dir, "revssh.lnk"), target, directory)


def create_crontab(crontab):
    if crontab_exists(crontab):
        return True
    else:
        logger.info("Creating crontab: " + crontab)
        output = subprocess.Popen('(crontab -l 2>/dev/null; echo \"' + crontab + '\") | crontab -',
                                  stdout=subprocess.PIPE, shell=True)
        return output.returncode == 0


def crontab_exists(crontab):
    output = subprocess.Popen("crontab -l", stdout=subprocess.PIPE, shell=True)
    return crontab in output.communicate()[0]
