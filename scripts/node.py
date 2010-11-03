from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.application.internet import MulticastServer
import couchdb
import hashlib
import string
import socket

class Node(DatagramProtocol):    

	s = None
	db = None
	myip = ''

	def __init__(self, ip):
		print 'Opening database...'
		self.myip = ip
		self.s = couchdb.Server('http://' + self.myip + ':5984')
		self.db = self.s['fsb-test']
	

	#Join group 224.0.0.1
	def startProtocol(self):
		print 'Joining multicast group...'
		self.transport.joinGroup('224.0.0.1')


	#sendHash
	def sendHash(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		myverstring = self.hashFun(self.db)
		print 'Sending hash...'
		sock.sendto(myverstring, ("224.0.0.1", 8888))
		sock.close()


	# Multicast a version string
	def datagramReceived(self, datagram, address):
		print 'Received hash string'
		if self.evalHashString(repr(datagram), address) is False:
			# pull from remote database
			self.replicateDB("http://" + address[0] + ":5984/fsb-test", "fsb-test")
			

	#Creates hash to transmit to other nodes
	def hashFun(self, db):
		print 'Generating hash...'
		hexnum = 0
		for doc in db:
			hexnum += int(string.split(db[doc].rev, '-')[1], 16)
		return hashlib.md5(str(hexnum)).digest()

	def evalHashString(self, datagram, address):
		print 'Evaluating hash string...'
		info = string.split(repr(datagram), ':')
		recvdhash = info[0]	
		if recvdhash is self.hashFun(self.db):
			return True
		if recvdhash is not self.hashFun(self.db):
			return False

	def replicateDB(self, source, target):
		print 'Replicating database...'
		self.s.replicate(source, target, continuous=False)

