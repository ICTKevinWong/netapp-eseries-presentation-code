"""
Showcases a simple wrapper around the request library.

We recommend the top functions. The combination of REST endpoints denotes a full workflow to utilize.

In the lowermost functions, there is a 1:1 function to REST endpoint wrapper, this is another way to
formulate an API client.
"""
import logging
from models import Session
from models import Requests


class RestApiException(Exception):
    """Specific exception for RestAPI unexpected status code errors"""


class CommandWrapper:
    logging.basicConfig(level=logging.INFO)

    def __init__(self, web_server_address: str,
                 storage_configuration_name: str,
                 secure=False):
        https = ''
        if secure:
            https = 's'

        self.base_url = ('http{}://{}/devmgr/v2/storage-systems/{}'
                         .format(https, web_server_address, storage_configuration_name))
        self.session = Session.get_default_session()
        self.log = logging.getLogger(__name__)

    def exp_create_volume(self, drive_count):
        """
        From the drive count, gets a list of available drives and creates a volume group and volume.
        :param drive_count: amount of drives to be used in the volume group
        :return: the reference to the created volume.
        """
        drive_list = self.get_usable_drives(drive_count)

        # Create volume groups/ storage pools
        volume_group_ref = self.create_volume_group(drive_list)
        volume_ref = self.create_volume(volume_group_ref)
        return volume_ref

    def get_usable_drives(self, drive_count):
        drives = self.get_drive_list().json()

        # Get a list of drives
        drive_list = []
        for drive in drives:
            if len(drive_list) < drive_count:
                if drive['available']:
                    drive_list.append(drive['driveRef'])
        return drive_list

    def create_volume(self, volume_group_reference):
        """
        Creates a volume
        :param volume_group_reference: volumeGroup reference ID to place the volume on
        :return: volumeReference ID
        """
        volume_ret = self.post_volume(volume_group_reference, 'presentation_vol_1')
        if volume_ret.status_code > 299:
            self.log.error('Failed to create volume. Return {}'.format(volume_ret.json()))
            raise RestApiException('Failed to create the volume. Error message {}'.format(volume_ret.json()))
        return volume_ret.json()['volumeRef']

    def create_volume_group(self, drive_id_list):
        """
        Creates a volume group using the given list of drive IDs

        :param drive_id_list: list of drive IDs to use
        :return: the created volume group reference
        """
        volume_group = self.post_storage_pool(drive_id_list)
        if volume_group.status_code > 299:
            self.log.error("Retrieved error message! \n{}".format(volume_group.json()))
            raise RestApiException('Failed to create volume group {}'.format(volume_group.json()))
        return volume_group.json()['volumeGroupRef']

    def set_controllers_optimal(self, controller_ref):
        url = '{}/symbol/setControllerToOptimal'.format(self.base_url)
        return self.session.post(url, json=controller_ref)

    def set_controllers_failed(self, controller_ref):
        url = '{}/symbol/setControllerToFailed'.format(self.base_url)
        return self.session.post(url, json=controller_ref)

    def set_drive_optimal(self, drive_ref):
        url = '{}/symbol/setDriveToOptimal'.format(self.base_url)
        return self.session.post(url, json=drive_ref)

    def set_drive_failed(self, drive_ref):
        url = '{}/symbol/setDriveToFailed'.format(self.base_url)
        return self.session.post(url, json=drive_ref)

    def get_controller_info(self):
        url = '{}/controllers'.format(self.base_url)
        return self.session.get(url)

    def get_analyzed_volume_stats(self, volume_ref):
        url = '{}/analysed-volume-statistics/{}'.format(self.base_url, volume_ref)
        return self.session.get(url)

    def get_drive_list(self):
        url = '{}/drives'.format(self.base_url)
        return self.session.get(url)

    def get_volumes(self):
        url = '{}/volumes'.format(self.base_url)
        return self.session.get(url)

    def post_volume(self, volume_group_reference, name):
        url = '{}/volumes'.format(self.base_url)
        payload = Requests.CreateVolumeRequest(volume_group_reference, name)
        return self.session.post(url, json=vars(payload))

    def get_storage_pool(self):
        url = '{}/storage-pools'.format(self.base_url)
        return self.session.get(url)

    def post_storage_pool(self, drive_id_list):
        payload = Requests.CreateStoragePoolRequest(drive_id_list)
        url = '{}/storage-pools'.format(self.base_url)
        return self.session.post(url, json=vars(payload))

    def delete_storage_pool(self, volume_group_ref):
        url = '{}/storage-pools/{}'.format(self.base_url, volume_group_ref)
        return self.session.delete(url)
