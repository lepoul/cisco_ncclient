import logging
import cisco_client.operations
import cisco_client.transport


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Higher Level of NETCONF client

class Manager:
    def __init__(self, ip, username, password):
        self.__session = None
        self.ip = ip
        self.username = username
        self.password = password
    # Connect to a device given its IP and user/pass credentials
    def connect(self):
        s = cisco_client.transport.Session(ip=self.ip, username=self.username, password=self.password)
        s.set_channel()
        s.hello_netconf()
        self.__session = s
    # Send an Edit config RPC
    def edit_config(self, filename):
        # command in <cmd>mpla mpla</cmd> format
        rpc = cisco_client.operations.EditConfigRPC()
        rpc.build_rpc(filename)
        self.__session.send_rpc(rpc.text)
        logger.info("Configuration pushed")
        self.__session.close()
    def is_connected(self):
        if self.__session:
            return True
        else:
            return False
    # Get running config
    # Using plain SSH, not NETCONF
    def get_config(self):
        temp_chan = cisco_client.transport.Session(ip=self.ip, username=self.username, password=self.password)
        temp_chan.set_channel()
        config = temp_chan.command("sh run | begin version")
        temp_chan.close()
        return config

