"""
Common python file to access/create a season. If authentication is not too big of an issue,
this could be very useful.
"""

import requests
import requests.packages.urllib3


def get_default_session():
    """
    Returns a request session for the SANtricity RestAPI Webserver
    """
    return get_session('rw', 'rw')


def get_session(username, password):
    """
    Returns a request session for the SANtricity RestAPI Webserver
    """
    request_session = requests.Session()
    # Default credentials
    request_session.auth = (username, password)
    request_session.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    # Ignore the self-signed certificate issues for https
    request_session.verify = False
    return request_session
