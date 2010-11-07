from node import Node
import time
import threading

class HashSender(threading.Thread):
	
	def __init__(self):
		n = Node()

	def run(self):
		while True:
			time.sleep(30)
			n.sendHash()


	
