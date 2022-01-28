import subprocess
import ssh_tools
import time
import threading
import logger


class Tunnel:

    def __init__(self, port, user, ip):
        self.PUBLIC_PORT = port
        self.RECEIVER_USER = user
        self.PUBLIC_IP = ip
        self.tunneling_port = None
        self.tunnel_thread = None

    def setup_tunnel(self, port):
        if ssh_tools.add_to_known_hosts(self.PUBLIC_IP, self.PUBLIC_PORT):
            if self.tunnel_thread is None or not self.tunnel_thread.is_alive():
                logger.info("Starting tunnel thread")
                self.tunnel_thread = threading.Thread(target=self.start_tunnel, args=port)
                self.tunnel_thread.start()
        else:
            logger.error("Could not add key to known hosts")

    def start_tunnel(self, port):
        logger.info("Starting tunnel at port: " + str(port))
        pipe = subprocess.Popen(
            "ssh -p " + self.PUBLIC_PORT + " -N -R " + str(
                port) + ":localhost:22 " + self.RECEIVER_USER + "@" + self.PUBLIC_IP,
            stdout=subprocess.PIPE, shell=True)
        pipe.communicate()
        logger.warning("Tunnel command exited")
        time.sleep(10)

