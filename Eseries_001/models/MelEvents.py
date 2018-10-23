"""
MelEvents object.

One way to go about an API client is to be more object oriented like this.
The Requests library is abstracted out and getting the mel events is as easy as calling
<get_mel_events>.
"""

from models import Session


class MelEvents:
    """Mel Events query parameters"""
    def __init__(self, count: int,
                 ip_address='localhost:8443',
                 storage_array='1',
                 critical=True,
                 include_debug=True,
                 start_sequence_number=-1):
        self.count = count
        self.critical = critical
        self.includeDebug = include_debug
        self.startSequenceNumber = start_sequence_number
        self.url = ('https://{}/devmgr/v2/storage-systems/{}/mel-events'
                    .format(ip_address, storage_array))

    def get_query_params(self):
        return {'count': self.count,
                'critical': self.critical,
                # 'includeDebug': self.includeDebug,
                'includeDebug': None,
                'startSequenceNumber': self.startSequenceNumber}

    def get_mel_events(self):
        session = Session.get_default_session()
        return session.get(url=self.url, params=self.get_query_params())

    def delete_mel_events(self, clear_cache=True, reset_mel=False):
        session = Session.get_default_session()
        payload = {'clearCache': clear_cache,
                   'reset_mel': reset_mel}
        return session.get(url=self.url, parameters=payload)
