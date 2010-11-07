from NodeListener import NodeListener
from HashSender import HashSender
from node import Node

class NodeService():
	NL = NodeListener()
	HS = HashSender()

	def __init__(self):
		HS.start()
		NL.start()

