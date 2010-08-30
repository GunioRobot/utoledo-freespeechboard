from socket import *
host = "localhost"
port = 21567
buf = 1024
addr = (host, port)

UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

while 1:
	data, addr = UDPSock.recvfrom(buf)
	if not data:
		print "Client has exited!"
		break
	else:
		print "\nReceived message '", data, "'"

UDPSock.close()
