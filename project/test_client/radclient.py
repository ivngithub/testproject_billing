import os, time
from collections import namedtuple

import pyrad.tools
from pyrad.client import Client
from pyrad.dictionary import Dictionary
import pyrad.packet


app_dir = os.path.abspath(os.path.dirname(__file__))

User = namedtuple('User', ['name', 'password', 'session_id'])

class RadUser:
    dictionary_file = os.path.join(app_dir, 'dictionary')
    NAS_Identifier = '127.0.0.1'
    NAS_IP_Address = '127.0.0.1'
    NAS_Port = 890

    def __init__(self, server="freeradius", secret="testing123",
                       user=User(name='fredf', password='wilma', session_id='1234567-Q-890')):
        self.server_name = server
        self.server_secret = bytes(secret, encoding='utf-8')
        self.user=user
        self.server = self._set_server()

    # srv = Client(server="freeradius", secret=b"testing123", dict=Dictionary("dictionary"))
    def _set_server(self):
        return Client(server=self.server_name, secret=self.server_secret, dict=Dictionary(self.dictionary_file))

    # req = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest, User_Name="fredf", NAS_Identifier="localhost")
    def _create_request_auth_packet(self):
        request = self.server.CreateAuthPacket(code=pyrad.packet.AccessRequest,
                                               User_Name=self.user.name,
                                               NAS_Identifier=self.NAS_Identifier)

        request["User-Password"] = request.PwCrypt(self.user.password)

        return request

    def _create_request_acct_packet(self, type_packet):

        request = self.server.CreateAcctPacket(code=pyrad.packet.AccountingRequest,
                                               User_Name=self.user.name,
                                               Acct_Status_Type='Start',
                                               NAS_IP_Address=self.NAS_IP_Address,
                                               Acct_Session_Id=self.user.session_id,
                                               NAS_Port=self.NAS_Port,
                                               NAS_Identifier=self.NAS_Identifier)

        if type_packet == 'update':
            request['Acct-Status-Type'] = 'Stop'
        elif type_packet == 'stop':
            request['Acct-Status-Type'] = 'Interim-Update'

        return request

    # response = self.server.SendPacket(req)
    def request(self, type_request=None):
        if type_request:
            return self.server.SendPacket(self._create_request_acct_packet(type_request))

        return self.server.SendPacket(self._create_request_auth_packet())


def view_result(client):

    result = client.request()

    if result.code == pyrad.packet.AccessAccept:
        print("access accepted")
    else:
        print("access denied")

    print("Attributes returned by server:")
    for i in result.keys():
        print('{}: {}'.format(i, result[i]))


user_bad = RadUser(user=User(name='fr', password='wilm', session_id='0000-Q-890'))
user_bob = RadUser(user=User(name='bob', password='wilma2', session_id='00w-Q-890'))
user_marianna = RadUser(user=User(name='marianna', password='wilma3', session_id='00w-Q-890'))

user_bad_r_auth = user_bad.request()
user_bad_r_acct = user_bad.request(True)

user_bob_r_auth = user_bob.request()
user_bob_r_acct = user_bob.request(True)
time.sleep(1)
user_bob_r_acct_upd = user_bob.request('update')
time.sleep(1)
user_bob_r_acct_stp = user_bob.request('stop')
time.sleep(1)

user_marianna_r_auth = user_marianna.request()
user_marianna_r_acct = user_marianna.request(True)
user_marianna_r_acct_upd = user_marianna.request('update')
user_marianna_r_acct_stp = user_marianna.request('stop')


if __name__ == '__main__':
    user = RadUser()
    view_result(user)
