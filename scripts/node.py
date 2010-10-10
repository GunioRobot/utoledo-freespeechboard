from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.application.internet import MulticastServer
import couchdb
import hashlib
import string
import socket

class Node(DatagramProtocol):    

	s = couchdb.Server()
	db = s['fsb-test']

	def __init__(self):
		s = couchdb.Server()
		db = s['fsb-test']
	

	#Join group 224.0.0.1
	def startProtocol(self):
		self.transport.joinGroup('224.0.0.1')


	#sendHash
	def sendHash(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		myverstring = self.hashFun(self.db)
		sock.sendto(myverstring, ("224.0.0.1", 8888))
		sock.close()


	# Multicast a version string
	def datagramReceived(self, datagram, address):
		if self.evalHashString(repr(datagram), address) is False:
			self.replicateDB("http://127.0.0.1:5984/", "http://" + address[0] + ":5984/")
			

	#Creates hash to transmit to other nodes
	def hashFun(self, db):
		hexnum = 0
		for doc in db:
			hexnum += int(string.split(db[doc].rev, '-')[1], 16)
		return hashlib.md5(str(hexnum)).digest()

	def evalHashString(self, datagram, address):
		info = string.split(repr(datagram), ':')
		recvdhash = info[0]	
		if recvdhash is self.hashFun(self.db):
			return True
		if recvdhash is not self.hashFun(self.db):
			return False

	def replicateDB(self, source, target):
		#need to fill code in in this section to
		#make sure the order is correct
		self.s.replicate(source, target, continuous=False)

