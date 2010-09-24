#!/usr/bin/python

import time
import couchdb
import cgi
import cgitb
cgitb.enable()					# enable debugging

form = cgi.FieldStorage()

if 'newmsg' in form:
	couch = couchdb.Server()		# connect to server

	if 'fsb-test' in couch:
		db = couch['fsb-test']		# get database
	else:
		db = couch.create('fsb-test')	# or create new database

	if 'thread0' in db:
		doc = db['thread0']		# get document
	else:
		doc = {}			# or create new document

	# add new message to working copy of document
	doc[str(len(doc))] = {'timestamp': time.time(), 'message': form["newmsg"].value}

	# replace old copy in database with working copy
	db['thread0'] = doc

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

