#!/usr/bin/python

from node import Node
from twisted.internet import reactor

n = Node('192.168.1.107')
reactor.listenMulticast(8888, n)
reactor.run()
