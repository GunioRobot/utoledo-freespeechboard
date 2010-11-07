import threading
from node import Node
from twisted.internet import reactor

class NodeListener(threading.Thread):

	n = None

	def __init__(self):
		self.n = Node()
	
	def run(self):
		reactor.listenMulticast(8888, self.n)
		reactor.run()

