from pyrad.client import Client
from pyrad.dictionary import Dictionary
import pyrad.packet

srv = Client(server="freeradius", secret=b"testing123", dict=Dictionary("dictionary"))

req = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest, User_Name="testing", NAS_Identifier="localhost")
req["User-Password"] = req.PwCrypt("wilma")

reply = srv.SendPacket(req)

if reply.code == pyrad.packet.AccessAccept:
    print("access accepted")
else:
    print("access denied")

print("Attributes returned by server:")
for i in reply.keys():
    print("%s: %s" % (i, reply[i]))