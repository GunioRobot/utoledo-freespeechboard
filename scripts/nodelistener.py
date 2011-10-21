import threading
from node import Node
from twisted.internet import reactor

class NodeListener(threading.Thread):

	n = None

	def __init__(self):
		self.n = Node()
		super(NodeListener,self).__init__()

	def run(self):
		print 'Starting listener thread...'
		reactor.listenMulticast(8888, self.n)
		reactor.run()

