"""
PART 2:
Showcases a little more advanced organization of an API client.

1) Utilize objects to create POST JSON payloads in the HTTP request.
    devicePayload = DeviceAlerts(True, ['kevin.wong@netapp.com'])
    response = SESSION.post(DEVICE_ALERTS_URL, json=vars(devicePayload))

2) Utilize objects to create POST JSON payloads and abstract the Request library out completely.
    melEventModel = MelEvents(10)
    response = melEventModel.get_mel_events()


The object oriented style stated in #2 is a style some developers prefer.


This script also showcases the use of E-series monitoring endpoints.


Major Event Log (MEL) are usually hardware based events that are fetched, cached, and stored in the REST API.
There are no changes performed on them from SYMbol.

Device Alerts is a system which will email a shortened variation of some MEL events if they occur. This script
covers the basics on how it is configured.
    Date: Sep 17, 2018 5:18:14 PM

    User-Supplied Information
    false

    Summary
    Node ID: ictm1301s02c4
    Host IP Address: xx.xxx.xxx.xxx
    Host ID: yyyyyyyy-a.zzz.z.netapp.com
    Event Error Code: 400c
    Event occurred: Mon, 17 Sep 2018 17:21:20 +0000
    Event Message: Controller placed offline Event Priority: Informational Component Type: Controller Component Location: Tray 0, Slot B

Events are closer in the REST API and will create events based on situations such as changes to a storage-arrays object graph.

Analyzed Statistics and Raw Statistics provide information on the statistics of a particular system
    The recommendation is to use Analyzed Statistics


"""

__author__ = 'kevin5'

import logging
import requests
import requests.packages.urllib3
from pprint import pprint

from models.DeviceAlerts import DeviceAlerts
from models.MelEvents import MelEvents

# CONSTANTS
WEBSERVER_IP = '1.1.1.1:8080'

USERNAME = 'rw'
PASSWORD = 'rw'

STORAGE_ARRAY = '1'

BASE_URL = 'https://{}/devmgr/v2/storage-systems'.format(WEBSERVER_IP)

# Logging
logging.basicConfig(level=logging.INFO)
requests.packages.urllib3.disable_warnings()
LOG = logging.getLogger(__name__)

# URIs
MEL_EVENTS_URL = '{}/{}/mel-events'.format(BASE_URL, STORAGE_ARRAY)
DEVICE_ALERTS_URL = '{}/{}/device-alerts'.format(BASE_URL, STORAGE_ARRAY)
ANALYZED_DRIVE_STATISTICS_URL = '{}/{}/analysed-drive-statistics'.format(BASE_URL, STORAGE_ARRAY)
DRIVE_STATISTICS_URL = '{}/{}/drive-statistics'.format(BASE_URL, STORAGE_ARRAY)
EVENTS_URL = '{}/{}/events'.format(BASE_URL, STORAGE_ARRAY)

#######################
# HELPER FUNCTIONS#####
########################


def append_query_parameter(query_parameters):
    """
    Unnecessary due to requests library. This showcases a basic method for adding on the query
    parameters in general.

    Takes in a dictionary of query parameters and outputs a query string
    :param query_parameters: dictionary of query parameters
    :return: appended query parameter string
    """
    query_ret = ''
    is_first_query_parameter = True
    for param in query_parameters:
        if query_parameters[param]:
            # The first query parameter needs a question mark to denote the existence of a query parameter
            if is_first_query_parameter:
                query_ret += '?'
                is_first_query_parameter = False
            else:
                query_ret += '&'
            query_ret += (param + '=' + str(query_parameters[param]))
    return query_ret


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

    # POST a Device Alert configuration
    devicePayload = DeviceAlerts(True, ['kevin.wong@netapp.com'])

    # Output the object as a dictionary. Can also use devicePayLoad.__dict__
    response = SESSION.post(DEVICE_ALERTS_URL, json=vars(devicePayload))
    if response.status_code > 299:
        raise RuntimeError("Failed to create device-alert configuration! {}".format(response.json()))

    # GET the current Device Alert configuration, it should conform to the POST model above.
    response = SESSION.get(DEVICE_ALERTS_URL)
    pprint(response.json())

    # MEL Method 1
    melEventModel = MelEvents(10)
    response = SESSION.get(MEL_EVENTS_URL, params=melEventModel.get_query_params())
    LOG.info("statusCode of GET melEvents: {}".format(response.status_code))

    # MEL Method 2
    melEventModel = MelEvents(10)
    response = melEventModel.get_mel_events()
    LOG.info("statusCode of GET melEvents: {}".format(response.status_code))

    # GET events and print out the first 3 events.
    response = SESSION.get(EVENTS_URL)
    for i in range(3):
        pprint(response.json()[i])

    # GET the drive/ analyzed drive statistics
    response = SESSION.get(ANALYZED_DRIVE_STATISTICS_URL).json()
    pprint(response[0])
    LOG.info('#' * 50)
    pprint(SESSION.get(DRIVE_STATISTICS_URL).json()[0])
