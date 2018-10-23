"""
PART 1:

This showcases the very basics of the E-Series REST API with Python and Requests.

It is not intended to be a guide on how to create an API client. It is intended to be used
to showcase how to create volumes and volume groups on a basic level with the Requests library.

At this time the recommended platform for such operations is by using Ansible.

See:
https://docs.ansible.com/ansible/latest/modules/list_of_storage_modules.html

"""

__author__ = 'kevin5'

import logging
import requests
import requests.packages.urllib3
from pprint import pprint


# CONSTANTS
WEBSERVER_IP = 'localhost:8080'
POOL_NAME = "presentation_pool_1"

DRIVE_COUNT = 2

USERNAME = 'rw'
PASSWORD = 'rw'

BASE_URL = 'http://{}/devmgr/v2/storage-systems'.format(WEBSERVER_IP)


# Logging
logging.basicConfig(level=logging.INFO)
requests.packages.urllib3.disable_warnings()
LOG = logging.getLogger(__name__)

#######################
# HELPER FUNCTIONS#####
########################


def get_session():
    """
    Returns a request session for the SANtricity RestAPI Webserver
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

    STORAGE_ARRAY_LIST = ['2', '3']
    LOG.info("Storage arrays {}".format(STORAGE_ARRAY_LIST))
    for storageArray in STORAGE_ARRAY_LIST:
        LOG.info("Working on array {}".format(storageArray))
        driveList = SESSION.get('{}/{}/drives'.format(BASE_URL, storageArray)).json()

        # Find the first available drives to use in my volume group
        driveIdList = []
        for drive in driveList:
            if len(driveIdList) < DRIVE_COUNT:
                if drive['available']:
                    driveIdList.append(drive['driveRef'])

        storagePoolPayload = {"raidLevel": "raid0",
                              "eraseSecuredDrives": True,
                              "diskDriveIds": driveIdList,
                              "name": POOL_NAME}
        url = ('{}/{}/storage-pools'.format(BASE_URL, storageArray))
        LOG.info(url)
        LOG.info(storagePoolPayload)
        volumeGroup = SESSION.post(url, json=storagePoolPayload)
        LOG.debug('Status code {}'.format(volumeGroup.status_code))

        if volumeGroup.status_code > 299:
            LOG.error("Retrieved error message! \n{}".format(volumeGroup.json()))
        else:
            LOG.info("volume group post json = {}".format(volumeGroup.json()))
            volumeGroupRef = volumeGroup.json()['volumeGroupRef']
            volumePayload = {'poolId': volumeGroupRef,
                             'name': 'presentation_vol_1',
                             'size': 20,
                             'segSize': 0}
            url = ('{}/{}/volumes'.format(BASE_URL, storageArray))
            response = SESSION.post(url, json=volumePayload)
            LOG.info("volume creation returned status code {} with body {}"
                     .format(response.status_code, response.json()))
            pprint(response.json())

            input("Press Enter to continue and delete the volume group...")
            url = ('{}/{}/storage-pools/{}'.format(BASE_URL, storageArray, volumeGroupRef))
            response = SESSION.delete(url)
            LOG.info("return status {}".format(response.status_code))
