from nodelistener import NodeListener
from hashsender import HashSender
from node import Node

class NodeService():
	NL = NodeListener()
	HS = HashSender()

	def __init__(self):
		self.HS.start()
		self.NL.start()

