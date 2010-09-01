#!/usr/bin/python

# Setup socket
from socket import *
host = "localhost"
port = 21567
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)

# Import the CGI module
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()

if "newmsg" not in form:
	msg = ""
else:
	msg = form["newmsg"].value

if msg:
	f = open('msg', 'w')	# only supporting one msg for now
	f.writeline(msg)
	f.close()
	UDPSock.sendto(msg, addr)
else:
	f = open('msg', 'r')
	msg = f.readline()
	f.close()


# Print the required header that tells the browser how to render the text.
print "Content-Type: text/html\n\n"

print "<head>"
print "<meta http-equiv=\"content-type\" content=\"text/xml; charset=utf-8\" />"

print "<title>Free Speech Board</title>"
print "</head>"

print "<body>"
print "<h1>Free Speech Board</h1>"
print msg
print "</br></br>"
print "<form action = \"addmsg.py\" method = \"get\">"
print "  Message:</br>"
print "  <textarea name=\"newmsg\" cols=60 rows=6></textarea></br>"
print "  <input type=\"submit\" value=\"Submit\" />"
print "</form>"
print "</body>"
print "</html>"

