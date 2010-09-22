#!/usr/bin/python

import time

import couchdb
#from couchdb.mapping import TextField, IntegerField, DateField, DictField

# Ideal document format, not implemented yet.
#class ThreadDoc(Document):
#	subject = TextField()
#	updated = DateTimeField(default=datetime.now)
#	messages = DictField(Mapping.build(
#		index = IntegerField(),
#		messageItem = DictField(Mapping.build(
#			timestamp = DateTimeField(default=datetime.now),
#			messageText = TextField()
#		))
#	))

# Import the CGI module
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()

if 'newmsg' in form:
	couch = couchdb.Server()
	if 'fsb-test' in couch:
		db = couch['fsb-test']
	else:
		db = couch.create('fsb-test')

	# Simplified code for testing:
	doc = {'timestamp': time.time(), 'message': form["newmsg"].value}
	db.create(doc)

# Print the required header that tells the browser how to render the text.
print "Content-Type: text/html\n\n"

print "<head>"
print "<meta http-equiv=\"content-type\" content=\"text/xml; charset=utf-8\" />"

print "<title>Free Speech Board</title>"
print "</head>"

print "<body>"
print "<h1>Free Speech Board</h1>"

if "newmsg" in form:
	print "<p>Added message: "
	if "newmsg" in form:
		print form["newmsg"].value
	print "</p>"

else:
	print "<p>Error: No message</p>"
print "</body>"
print "</html>"

