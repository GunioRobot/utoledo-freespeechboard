from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.application.internet import MulticastServer
import couchdb
import hashlib
import string
import socket
import fcntl
import struct
import pycurl
import sys

class Node(DatagramProtocol):    

	s = None
	db = None
	myip = None

	map_conflicts = '''function(doc) {
		if(doc._conflicts) {
			emit(doc._conflicts, null);
		}
	}'''

	# Taken from interwebz
	# Returns IPv4 Address
	def get_ip_address(self, ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915,struct.pack('256s', ifname[:15]))[20:24])


	def __init__(self):
		print 'Opening database...'
		self.myip = self.get_ip_address('wlan0')
		self.s = couchdb.Server('http://' + self.myip + ':5984')
		self.db = self.s['fsb-test']
		self.contents = ''	# for pycurl


	def body_callback(self, buf):	# for pycurl
		self.contents = self.contents + buf
	

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

	def resolveConflicts(self):
		print 'Checking for conflicts...'
		# check each document for conflicts
		res = self.db.query(self.map_conflicts)
		for row in res:
			# get revs for conflicting versions
			curl = pycurl.Curl()
			curl.setopt(curl.URL, 'http://' + self.myip + ':5984/fsb-test/' + row.id + '?open_revs=all')
			curl.setopt(curl.WRITEFUNCTION, self.body_callback)
			curl.perform()

			index = self.contents.find('_id')
			idnum1 = self.contents[index+6:index+38]
			index = self.contents.find('_rev', index)
			rev1 = self.contents[index+7:index+41]
			index = self.contents.find('_id', index)
			idnum2 = self.contents[index+6:index+38]
			index = self.contents.find('_rev', index)
			rev2 = self.contents[index+7:index+41]

			# get conflicting documents
			self.contents = ""
			curl.setopt(curl.URL, 'http://' + self.myip + ':5984/fsb-test/' + idnum1 + '?rev='+rev1)
			curl.perform()
			doc1 = couchdb.json.decode(self.contents)
			print doc1

			self.contents = ""
			curl.setopt(curl.URL, 'http://' + self.myip + ':5984/fsb-test/' + idnum2 + '?rev='+rev2)
			curl.perform()
			doc2 = couchdb.json.decode(self.contents)
			print doc2

			curl.close()

			# merge documents
			mergedoc = self.db[row.id]
			msgdict = dict()
			msgs = dict()
			for msg in doc1['msgs']:
				timestamp = str(doc1['msgs'][msg]['timestamp'])
				msgdict[timestamp] = doc1['msgs'][msg]['message']
			for msg in doc2['msgs']:
				timestamp = str(doc2['msgs'][msg]['timestamp'])
				msgdict[timestamp] = doc2['msgs'][msg]['message']
			index = 0
			for key in sorted(msgdict.iterkeys()):
				msgs[index] = {'timestamp': key, 'message': msgdict[key]}
				index = index + 1

			updatetime = doc1['updatetime']
			updatetime2 = doc2['updatetime']
			if updatetime2 > updatetime:
				updatetime = updatetime2

			mergedoc['msgs'] = msgs
			mergedoc['updatetime'] = updatetime
			
			# save merged document
			self.db[row.id] = mergedoc
			print 'Conflicts resolved!'


