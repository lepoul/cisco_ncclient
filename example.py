from cisco_client import manager
import logging


logging.basicConfig(level=logging.DEBUG)

# Define a device manager

alderaan = manager.Manager(ip="147.102.7.96", username="lefteris", password="W3llcome")
alderaan.connect()

if alderaan.is_connected():
    try:
        prev = alderaan.get_config()
        alderaan.edit_config('test_config.conf')
        cu = alderaan.get_config()
    except Exception as err:
        logging.error(err)
    if prev != cu:
        print("Changed")
    else: 
        print("Nothing changed")
else:
    print("xaireta mou ton platano")
