#!/usr/bin/python

import time
import couchdb
import cgi
import cgitb
cgitb.enable()					# enable debugging

form = cgi.FieldStorage()

if 'newtopic' in form:
	subject = form["newtopic"].value

	couch = couchdb.Server()		# connect to server

	if 'fsb-test' in couch:
		db = couch['fsb-test']		# get database
	else:
		db = couch.create('fsb-test')	# or create new database

	doc = {'subject': subject, 'createtime': time.time(), 'msgs': {}}	# create empty topic
	db[subject] = doc			# add new topic to database


# Print the required header that tells the browser how to render the text.
print "Content-Type: text/html\n\n"

print "<head>"
print "<meta http-equiv=\"content-type\" content=\"text/xml; charset=utf-8\" />"

print "<title>Free Speech Board</title>"
print "</head>"

print "<body>"
print "<h1>Free Speech Board</h1>"

if "newtopic" in form:
	print "<p>Added topic: "
	print form["newtopic"].value
	print "</p>"

else:
	print "<p>Error: No topic</p>"
print "</body>"
print "</html>"

