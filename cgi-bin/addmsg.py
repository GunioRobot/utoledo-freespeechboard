#!/usr/bin/python

import time
import couchdb
import cgi
import cgitb
import getip
cgitb.enable()					# enable debugging

form = cgi.FieldStorage()

couch = couchdb.Server('http://' + getip.get_ip_address('wlan0') + ':5984')		# connect to server
if 'fsb-test' in couch:
	db = couch['fsb-test']		# get database
else:
	db = couch.create('fsb-test')	# or create new database

# Print the required header that tells the browser how to render the text.
print "Content-Type: text/html\n\n"

print "<head>"
print "<meta http-equiv=\"content-type\" content=\"text/xml; charset=utf-8\" />"

print "<title>Free Speech Board</title>"
print "</head>"

print "<body>"
print "<h1>Free Speech Board</h1>"

for thread in form:

	if thread in db:
		doc = db[thread]		# get document
		msgs = doc['msgs']		# get msgs dict

		# add new message to working copy of document
		msgs[str(len(msgs))] = {'timestamp': time.time(), 'message': form[thread].value}

		doc['msgs'] = msgs		# store updated msgs in doc
		doc['updatetime'] = time.time()
		db[thread] = doc		# store updated doc in db

		print "<p>Added message: "
		print form[thread].value
		print "</p>"

	else:
		print "<p>Error: Thread"
		print thread
		print " not found!</p>"

print "</body>"
print "</html>"

