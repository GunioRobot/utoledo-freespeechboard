from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.application.internet import MulticastServer
import couchdb

class Node(DatagramProtocol):
    
    def __init__(self):
	s = Server()
	db = s['fsb-test']
	

    #Join group 224.0.0.1
    def startProtocol(self):
        self.transport.joinGroup('224.0.0.1')

    # Multicast a version string
    def sendVersion(self, datagram, address):
	#Need to get _rev for a *document*, not a db. Need to explore
	#this comparison issue further.
	myverstring = "Rev:" + db[_rev] + ";Address:" + address
        self.transport.write("Rev:12345;Address:123.456.78.910", address)

    def recvVersion(self, datagram, address):
	versionstring = repr(datagram)

    def replcateDB(self, source, target):
	#need to fill code in in this section to
	#make sure the order is correct
	s.replicate(source, target, False)
