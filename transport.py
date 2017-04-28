import socket
import paramiko
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# A hello message for NETCONF session

HELLO = '''<?xml version="1.0" encoding=\"UTF-8\"?>
<hello><capabilities>
     <capability>urn:ietf:params:netconf:base:1.0</capability>
      <capability>urn:ietf:params:netconf:capability:writeable-running:1.0</capability>
       <capability>urn:ietf:params:netconf:capability:rollback-on-error:1.0</capability>
        <capability>urn:ietf:params:netconf:capability:startup:1.0</capability>
         <capability>urn:ietf:params:netconf:capability:url:1.0</capability>
        <capability>urn:cisco:params:netconf:capability:pi-data-model:1.0</capability>
       <capability>urn:cisco:params:netconf:capability:notification:1.0</capability>
   </capabilities>
</hello>]]>]]>'''

# A message for closing NETCONF session

CLOSE = '''
<?xml version="1.0" encoding=\"UTF-8\"?>
<rpc message-id="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <close-session/>
</rpc>]]>]]>'''


class Session:
    def __init__(self, ip, username, password):
        self.__ip = ip
        self.__username = username
        self.__password = password
        self.channel = None

    def set_channel(self):
        logger.info("Connecting to the server")
#   Defining an SSH client to handle NETCONF connection
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#   Socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.__ip, 22))
#   Paramiko transport handler
        trans = paramiko.Transport(s)
        trans.connect(username=self.__username, password=self.__password)
        trans.set_keepalive(60)
#   Gets a paramiko.Channel object
        c = trans.open_session(window_size=100000)
        self.channel = c

# Send the NETCONF HELLO message to the device
    def hello_netconf(self):
        if self.channel:
            self.channel.invoke_subsystem("netconf")
            self.channel.send(HELLO)
            rep = self.channel.recv(4096)
            logger.debug(rep)
        else:
            logger.info("Need to establish connection first")

# RPC Sender Function
    def send_rpc(self, rpc):
        logger.info("Preparing to send RPC")
        if self.channel.send_ready():
            logger.info(rpc)
            # Send the RPC
            self.channel.send(rpc)
            reply = self.channel.recv(4096)
            reply = reply.decode('utf-8')
            # Check Reply for <ok> element
            if "ok" in reply:
                logger.info("RPC sent succesfully")
            elif "error" in reply:
                logger.info("Server error")
                logger.debug(reply)
        else:
            logger.info("Channel is down")

# Send CLOSE message to end the session
    def close(self):
        logger.info("Closing session")
        try:
            self.send_rpc(CLOSE)
            self.channel.close()
        except Exception as err:
            logger.error(err)

# Send commands using plain SSH
    def command(self, com):
        if self.channel.send_ready():
            config = ''
            try:
                # Paramiko's exec_command
                self.channel.exec_command(com)
                while True:
                    data = self.channel.recv(100000)
                    data = data.decode('utf-8')
                    config += data
                    if data == '':
                        break
                return config
            except Exception as err:
                logger.error(err)
        else:
            logger.error("Channel error")

