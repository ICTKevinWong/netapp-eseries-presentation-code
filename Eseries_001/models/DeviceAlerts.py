""""
Payload wrapper around DeviceAlerts POST configuration.

The idea here is to provide object oriented 'reasonable defaults' for a particular
client API. In this case smtp.netapp.com is a common smtp server for NetApp employees; not so much
for others.

"""

class DeviceAlerts:

    def __init__(self, alerting_enabled: bool,
                 recipient_email_addresses: list,
                 email_server_address: str = 'smtp.netapp.com',
                 email_sender_address: str = 'kevin5test@netapp.com',
                 send_additional_contact_information: bool = True,
                 additional_contact_information: bool = False):
        self.alertingEnabled = alerting_enabled
        self.emailServerAddress = email_server_address
        self.emailSenderAddress = email_sender_address
        self.sendAdditionalContactInformation = send_additional_contact_information
        self.additionalContactInformation = additional_contact_information
        self.recipientEmailAddresses = recipient_email_addresses
