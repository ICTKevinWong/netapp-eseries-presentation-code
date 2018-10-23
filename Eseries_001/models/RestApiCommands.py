"""
If one wants more flexibility in their REST API command wrapper, they can simply provide the URL instead and let
the user handle the Requests library themselves. This allows the users to have a little more control
in exchange for complexity. Clients can then utilize request hooks as well.
"""


class RestApiCommands:
    def __init__(self, web_server_address: str,
                 storage_configuration_name: str):
        self.base_url = ('http://{}/devmgr/v2/storage-systems/{}'
                         .format(web_server_address, storage_configuration_name))

    def set_controllers_optimal(self):
        return '{}/symbol/setControllerToOptimal'.format(self.base_url)

    def set_controllers_failed(self):
        return '{}/symbol/setControllerToFailed'.format(self.base_url)

    def set_drive_optimal(self):
        return '{}/symbol/setDriveToOptimal'.format(self.base_url)

    def set_drive_failed(self):
        return '{}/symbol/setDriveToFailed'.format(self.base_url)

    def get_controller_info(self):
        return '{}/controllers'.format(self.base_url)

    def get_analyzed_volume_stats(self, volume_ref):
        return '{}/analysed-volume-statistics/{}'.format(self.base_url, volume_ref)

    def get_drive_list(self):
        return '{}/drives'.format(self.base_url)

    def get_volumes(self):
        return '{}/volumes'.format(self.base_url)

    def post_volume(self):
        return '{}/volumes'.format(self.base_url)

    def get_storage_pool(self):
        return '{}/storage-pools'.format(self.base_url)

    def post_storage_pool(self):
        return '{}/storage-pools'.format(self.base_url)

    def delete_storage_pool(self, volume_group_ref):
        return '{}/storage-pools/{}'.format(self.base_url, volume_group_ref)


def get_rest_api_commands(web_server_address, storage_configuration_name):
    return RestApiCommands(web_server_address, storage_configuration_name)
