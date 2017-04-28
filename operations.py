import logging
from os.path import isfile


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

NETCONF_WRAP = '''
<?xml version="1.0" encoding="UTF-8"?>
<rpc message-id ="101" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <edit-config>
    <target><running/></target>
    <config>
        <cli-config-data>
%s</cli-config-data>
    </config>
    </edit-config>
</rpc>]]>]]>'''

# An Edit Configuration RPC object
class EditConfigRPC:
    def __init__(self):
        # CLI command or block of commands
        self.text = None

# Config block must be of format:
# <cmd>mpla mpla</cmd>

    def build_rpc(self, file):
        try:
            # Open configuration file
            a = open(file, 'r+')
            logger.info("Constructing RPC")
            wrapper = '\t<cmd>%s</cmd>\n'
            config_block = ''
            # Include every line of config file
            for line in a.readlines():
                line = line.replace('\n', '')
                command = wrapper % line
                config_block += command
            # Wrap RPC
            rpc = NETCONF_WRAP % config_block
            logger.debug(rpc)
            logger.info("RPC ready to send")
            self.text = rpc
        except isfile(file) == False:
            logger.info("%s not a valid filename" % file)
