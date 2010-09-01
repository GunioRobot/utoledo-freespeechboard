from socket import *
host = "localhost"
port = 21567
buf = 1024
addr = (host, port)

UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

while 1:
	data, addr = UDPSock.recvfrom(buf)
	if data:
		f = open('msg', 'w')	# only supporting one msg for now
		f.writeline(data)
		f.close()

