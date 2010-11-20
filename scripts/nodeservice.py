from nodelistener import NodeListener
from hashsender import HashSender
from node import Node

class NodeService():

	NL = None
	HS = None

	def __init__(self):
		self.NL = NodeListener()
		self.HS = HashSender()
		self.HS.start()
		self.NL.start()

