"""
Sample script on a variety of information gathering calls

Storage System base information
Volume information
Drive information
Hardware inventory
Object graph:
    The object graph is the large data package that the REST API receives from SYMbol or the E-Series
    Storage System backend API. If necessary, customers can utilize the whole object graph if there are
    more uncommon fields necessary

XPath filtered Object graph:
    A built-in convenience endpoint for filtering out the Object Graph.
"""

__author__ = 'kevin5'

import logging
import requests
import requests.packages.urllib3
from pprint import pprint


# CONSTANTS
WEBSERVER_IP = 'localhost:8080'

USERNAME = 'rw'
PASSWORD = 'rw'

STORAGE_ARRAY = '1'

BASE_URL = 'http://{}/devmgr/v2/storage-systems'.format(WEBSERVER_IP)

# Logging
logging.basicConfig(level=logging.INFO)
requests.packages.urllib3.disable_warnings()
LOG = logging.getLogger(__name__)

# URIs
STORAGE_SYSTEM_URL = '{}/{}'.format(BASE_URL, STORAGE_ARRAY)
VOLUME_URL = '{}/{}/volumes'.format(BASE_URL, STORAGE_ARRAY)
DRIVE_URL = '{}/{}/drives'.format(BASE_URL, STORAGE_ARRAY)
HARDWARE_INVENTORY_URL = '{}/{}/hardware-inventory'.format(BASE_URL, STORAGE_ARRAY)
OBJECT_GRAPH_URL = '{}/{}/graph'.format(BASE_URL, STORAGE_ARRAY)

XPATH_BASE_URL = '{}/{}/graph/xpath-filter?query='.format(BASE_URL, STORAGE_ARRAY)
# XPATH_URL = '{}/{}/graph/xpath-filter?query={}'.format(BASE_URL, STORAGE_ARRAY, '/sa/saData')
# XPATH_URL2 = '{}/{}/graph/xpath-filter?query={}'.format(BASE_URL, STORAGE_ARRAY, '/drive')


#######################
# HELPER FUNCTIONS#####
########################

def get_xpath_url(query):
    return XPATH_BASE_URL + query


def get_session():
    """
    responseurns a request session for the SANtricity RestAPI Webserver
    """
    request_session = requests.Session()
    # Default credentials
    request_session.auth = (USERNAME, PASSWORD)
    request_session.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    # Ignore the self-signed certificate issues for https
    request_session.verify = False
    return request_session

#######################
# MAIN FUNCTIONS#######
#######################


if __name__ == '__main__':
    SESSION = get_session()

    # Can use content for retrieving the contents in bytes or use .json() for retrieving the data in a dictionary

    response = SESSION.get(STORAGE_SYSTEM_URL)
    LOG.info('storageSystemResponse = {}'.format(response.content))
    LOG.info('length: {}'.format(len(response.content)))

    response = SESSION.get(VOLUME_URL)
    LOG.info('volumeResponse = {}'.format(response.content))
    LOG.info('length: {}'.format(len(response.content)))

    response = SESSION.get(DRIVE_URL)
    LOG.info('driveresponse = {}'.format(response.content))
    LOG.info('length: {}'.format(len(response.content)))
    pprint(response.json())

    # Get content in bytes because this call can return very large objects
    response = SESSION.get(HARDWARE_INVENTORY_URL)
    LOG.info('hardwareInventoryResponse = {}'.format(response.content))
    LOG.info('length: {}'.format(len(response.content)))

    # Get content in bytes because this call can return very large objects
    response = SESSION.get(OBJECT_GRAPH_URL)
    LOG.info('objectGraphResponse = {}'.format(response.json()))
    LOG.info('length: {}'.format(len(response.content)))

    # Get content in bytes because this call can return very large objects
    response = SESSION.get(get_xpath_url('/drive'))
    LOG.info('xPathResponse = {}'.format(response.json()))
    LOG.info('length: {}'.format(len(response.content)))

    # Get content in bytes because this call can return very large objects
    response = SESSION.get(get_xpath_url('/sa/saData'))
    LOG.info('xPathResponse = {}'.format(response.content))
    LOG.info('length: {}'.format(len(response.content)))
