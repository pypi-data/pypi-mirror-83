import requests
import json

class Client():
    """
    SleentO Client account manager class
    """
    def __init__(self, cid, auth_token, *args, **kwargs):
        """Authenticate

        :cid             : The client id
        :auth_token      : The authentication token
        """
        self.cid = cid
        self.auth_token = auth_token

    def __str__(self):
        return "Client id : {} , auth_token : {}".format(self.cid, self.auth_token)



class Message():
    """
    SleentO message manager class
    """

    def __init__(self, client, to_phone_number, body, *args, **kwargs):
        """Create a new message to send to end client

        :client            : An instance of Client(cid, auth_token)
        :to_phone_number : Receiver phone number eg. +243xxxxxxxxx
        :body            : The message body eg. Hello World !
        """
        self.client = client
        self.to_phone_number = to_phone_number
        self.body = body
        self._URL = "http://www.sleento.com/"

    def send(self):
        """Send sms to the server
        """
        body = {
            "cid"	: self.client.cid,
            "phone" : self.to_phone_number,
            "body"  : self.body
        }
        headers = {
            "Content-Type" : "application/json",
            "Authorization": "token {}".format(self.client.auth_token)
        }

        res = requests.post(url=self._URL + 'api/sms/', data=json.dumps(body),  headers=headers)

        return res


    def get(self, sms_id):
        """Get SMS by sms id

        :sms_id            : The unique sms identification
        """
        pass

    def filter(self, date, satus):
        """Filter sms 

        :date            : the date the sms was sent eg. 2020-08-22
        :status          : SMS status, sent, queue, unsent
        """
        pass

    def __str__(self):
        return "to_phone_number : {}, body : {}".format(
            self.to_phone_number, 
            self.body
        )