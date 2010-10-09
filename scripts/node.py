from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.application.internet import MulticastServer
import couchdb
import hashlib
import string

class Node(DatagramProtocol):    

	s = couchdb.Server()
	db = s['fsb-test']

	def __init__(self):
		s = couchdb.Server()
		db = s['fsb-test']
	

	#Join group 224.0.0.1
	def startProtocol(self):
		self.transport.joinGroup('224.0.0.1')


	# Multicast a version string
	def sendHash(self, datagram, address):
		#Need to get _rev for a *document*, not a db. Need to explore
		#this comparison issue further.
		myverstring = self.hashFun(self, self.db) + ":" + address
		self.transport.write(myverstring, address)

	#Creates hash to transmit to other nodes
	def hashFun(self, db):
		hexnum = 0
		for doc in db:
			hexnum += int(string.split(db[doc].rev, '-')[1], 16)
		return hashlib.md5(str(hexnum)).digest()

	def evalHashString(self, datagram, address):
		info = string.split(repr(datagram), ':')
		recvdhash = info[0]	
		if recvdhash is hashFun():
			return true
		if recvdhash is not hashFun():
			return false

	def replcateDB(self, source, target):
		#need to fill code in in this section to
		#make sure the order is correct
		s.replicate(source, target, False)

