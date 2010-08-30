from socket import *
host = "localhost"
port = 21567
buf = 1024
addr = (host, port)

UDPSock = socket(AF_INET, SOCK_DGRAM)
msg = "Dance like a ho"
UDPSock.sendto(msg, addr)
