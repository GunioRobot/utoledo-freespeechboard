#!/usr/bin/python

from node import Node
from twisted.internet import reactor

n = Node()
reactor.listenMulticast(8888, n)
reactor.run()
