#!/usr/bin/python

import time
import couchdb
import cgi
import cgitb
cgitb.enable()					# enable debugging

form = cgi.FieldStorage()

for thread in form:
	couch = couchdb.Server()		# connect to server

	if 'fsb-test' in couch:
		db = couch['fsb-test']		# get database
	else:
		db = couch.create('fsb-test')	# or create new database

	if thread in db:
		doc = db[thread]		# get document
		msgs = doc['msgs']		# get msgs dict

		# add new message to working copy of document
		msgs[str(len(msgs))] = {'timestamp': time.time(), 'message': form[thread].value}

		doc['msgs'] = msgs		# store updated msgs in doc
		db[thread] = doc		# store updated doc in db

# Print the required header that tells the browser how to render the text.
print "Content-Type: text/html\n\n"

print "<head>"
print "<meta http-equiv=\"content-type\" content=\"text/xml; charset=utf-8\" />"

print "<title>Free Speech Board</title>"
print "</head>"

print "<body>"
print "<h1>Free Speech Board</h1>"

foundThread = False
for thread in form:
	foundThread = True
	if thread in db:
		print "<p>Added message: "
		print form[thread].value
		print "</p>"
	else:
		print "<p>Error: Thread not found!</p>"
if not foundThread:
	print "<p>Error: No message</p>"
print "</body>"
print "</html>"

