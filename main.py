#!/usr/bin/env python
import codecs
import json
import sys
import time

import requests

import logger
import ssh_tools
import ssh_tunnel
import util

url = "192.168.1.101"
api_key = "test"
tunnel = ssh_tunnel.Tunnel("22", "user", url)


def start():
    logger.info("Starting reverse ssh tunnel")
    # cron.create_reboot_crontab()
    # cron.create_startup_crontab()
    while True:
        write_start_file()
        get_server_key()
        time.sleep(600)


# Write the last time the program has been run to file.
# If the application stops unexpectedly it can be restarted based on the time in this file.
def write_start_file():
    f = open(util.get_home_folder() + "/start.rsh", "w")
    f.write(str(time.time()))
    f.close()


# Get the ssh key of the server, so it can be used to start the tunnel
def get_server_key():
    if len(url) == 0:
        logger.error("Url not set. Config is not loaded. Exiting")
        sys.exit()

    base64_ssh_key = codecs.encode(ssh_tools.get_ssh_key().encode("utf-8"), 'base64').decode("utf-8") \
        .replace("\n", "").replace("\r", "")
    print("Base64 ssh key: " + base64_ssh_key)
    response = requests.get(
        url + '/getServerKey'
        , headers={
            "Auth": api_key,
            'sshKey': base64_ssh_key}
    )
    logger.info("Retrieved server ssh key")
    handle_server_info_response(response.content)


def handle_server_info_response(content):
    server_info = json.loads(content)
    if server_info["serverSshKey"]:
        ssh_tools.save_authorized_key(server_info["serverSshKey"])

    tunnel.setup_tunnel(server_info["tunnelPort"])


if __name__ == '__main__':
    if util.is_revssh_running():
        print("Already running")
        exit(0)
    else:
        print("Starting revssh")
        start()
