import util
import os
import subprocess
import logger


def get_ssh_key():
    home_folder = util.get_home_folder()
    path = home_folder + '/.ssh/id_rsa.pub'
    if os.path.exists(path):
        logger.info("Found existing ssh key")
        return open(path).read()
    else:
        if generate_ssh_key(home_folder):
            return get_ssh_key()
        else:
            logger.error("Error creating ssh keys")


def generate_ssh_key(home_folder):
    logger.warning("Generating ssh key")
    pipe = subprocess.Popen(
        "cat /dev/zero | ssh-keygen -q -N "" -t rsa -C " + util.get_username() + '@' + util.get_hostname() + ' -f ' + home_folder + '/.ssh/id_rsa',
        stdout=subprocess.PIPE)
    pipe.communicate()
    return pipe.returncode == 0


def save_authorized_key(key):
    path = util.get_home_folder() + "/.ssh/authorized_keys"
    if not os.path.exists(path):
        f = open(path, "a")
        f.close()
    read = open(path, "r")
    if key in read.read():
        return
    logger.info("Saving new server key in authorized keys")
    read.close()
    append = open(path, "a")
    append.write(key)


def key_in_known_hosts(ip):
    pipe = subprocess.Popen(
        "ssh-keygen -F " + ip,
        stdout=subprocess.PIPE, shell=True)
    pipe.communicate()
    return pipe.returncode == 0


def add_to_known_hosts(ip, port):
    path = util.get_home_folder() + "/.ssh/known_hosts"
    if not os.path.exists(path):
        open(path, 'a').close()

    if key_in_known_hosts(ip):
        logger.info("Server key is in known hosts")
        return True
    else:
        logger.warning("Server key is NOT in known hosts. Executing key scan")

    pipe = subprocess.Popen(
        "ssh-keyscan -H -p " + port + " " + ip + " >> " + path,
        stdout=subprocess.PIPE, shell=True)
    pipe.communicate()
    return pipe.returncode == 0
