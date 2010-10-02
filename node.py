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
	myverstring = "Rev:" + db[_rev] + ";Address:" + address
        self.transport.write("Rev:12345;Address:123.456.78.910", address)

    def recvVersion(self, datagram, address):
	versionstring = repr(datagram)

    def replcateDB(self, source, target):
	#Create a server object and set db to be the 'fsb-test' database
	s = Server()
	db = s['fsb-test']
	s.replicate(source, target, False)
