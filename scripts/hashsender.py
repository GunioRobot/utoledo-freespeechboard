from node import Node
import time
import threading

class HashSender(threading.Thread):

	n = None	

	def __init__(self):
		self.n = Node()
		super(HashSender,self).__init__()

	def run(self):
		print 'Starting hash sender thread...'
		while True:
			time.sleep(30)
			self.n.resolveConflicts()
			self.n.sendHash()



	
