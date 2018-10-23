"""
PART 3:

Showcases the use of a Command wrapper around REST endpoints.

This part also will demonstrate the uses of the REST API as a backend component for testing.

There are SYMbol APIs that have been wrapped up in the REST API.

Fail Controller - Sets a controller to a failed state

Optimize Controller - Sets the controller to get out of the manually triggered failed state
    If the controller is legitimately in a failed state, this won't save it.

Fail Drive - Sets a drive to a failed stated

Optimize Drive - Sets the drive to get out of the manually triggered failed state
    If the drive is legitimately in a failed state, this won't save it.


With these calls, we can induce a manually triggered failed state for testing purposes.

One thing to note is that there is a level of hardening in the REST API that is not performed for
SYMbol calls. Some calls may fail due to the timing of a storage array and not because of anything wrong with the state
of the system or with the request. Because of this, it is recommended that some SYMbol calls (such as the ones
above) are hardened in a retry mechanism.
"""


__author__ = 'kevin5'

import logging
import time
from models.CommandWrapper import CommandWrapper

# CONSTANTS
WEBSERVER_IP = 'localhost:8080'
STORAGE_ARRAY = '2'

DRIVE_COUNT = 3
MAX_FAIL_COUNT = 5

# Logging
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)


class RestApiException(Exception):
    """Specific exception for RestAPI unexpected status code errors"""

#######################
# MAIN FUNCTIONS#######
#######################


if __name__ == '__main__':
    # Create volume groups/ storage pools
    COMMAND_WRAPPER = CommandWrapper(WEBSERVER_IP, STORAGE_ARRAY)
    driveList = COMMAND_WRAPPER.get_usable_drives(DRIVE_COUNT)
    volumeGroupRef = COMMAND_WRAPPER.create_volume_group(driveList)
    volumeRef = COMMAND_WRAPPER.create_volume(volumeGroupRef)

    # Start the testing process
    try:
        SLEEP_TIME_SECONDS = 15
        input("Press Enter to continue the testing process")
        response = COMMAND_WRAPPER.get_analyzed_volume_stats(volumeRef)
        LOG.info('combined IOps: {}'.format(response.json()[0]['combinedIOps']))

        controllers = COMMAND_WRAPPER.get_controller_info()
        controllerToFail = controllers.json()[0]['controllerRef']

        LOG.info("Attempting to fail drive")
        response = COMMAND_WRAPPER.set_drive_failed(driveList[0])
        # response = SESSION.post(REST_API.set_drive_failed(), json=driveList[0])

        # Another way to check for status!
        response.raise_for_status()

        LOG.info("Attempting to fail controller")
        response = COMMAND_WRAPPER.set_controllers_failed(controllerToFail)
        response.raise_for_status()

        LOG.info("Sleeping for {} second(s)".format(SLEEP_TIME_SECONDS))
        time.sleep(SLEEP_TIME_SECONDS)

        response = COMMAND_WRAPPER.get_analyzed_volume_stats(volumeRef)
        LOG.info('combined IOps: {}'.format(response.json()[0]['combinedIOps']))

        LOG.info("Attempting to revive drive")
        for retryCount in range(MAX_FAIL_COUNT):
            response = COMMAND_WRAPPER.set_drive_optimal(driveList[0])
            if response.status_code > 299:
                LOG.error('we have failed to restore drive to optimal state! Return {}'.format(response.json()))
                if retryCount >= MAX_FAIL_COUNT:
                    raise RestApiException("we have failed to restore drive to optimal state!")

        LOG.info("Attempting to revive controller")
        for retryCount in range(MAX_FAIL_COUNT):
            response = COMMAND_WRAPPER.set_controllers_optimal(controllerToFail)
            if response.status_code > 299:
                LOG.error('we have failed to restore controller to optimal state! Return {}'.format(response.json()))
                if retryCount >= MAX_FAIL_COUNT:
                    raise RestApiException("we have failed to restore controller to optimal state!")

        input("Press Enter to delete the volume")
        response = COMMAND_WRAPPER.delete_storage_pool(volumeGroupRef)
        LOG.info("return status {}: {}".format(response.status_code, response.json()))

        LOG.info("Code ended successfully!")

    except RestApiException as error:
        LOG.exception(error)
        response = COMMAND_WRAPPER.delete_storage_pool(volumeGroupRef)
        LOG.info("return status {}".format(response.status_code))
