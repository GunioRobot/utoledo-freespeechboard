import socket
import fcntl
import struct

# Taken from interwebz
# Returns IPv4 Address
def get_ip_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915,struct.pack('256s', ifname[:15]))[20:24])

