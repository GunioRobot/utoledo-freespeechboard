#!/usr/bin/python

import time
import couchdb
import cgi
import cgitb
import getip
cgitb.enable()				# enable debugging

form = cgi.FieldStorage()
topicid = form['topicid'].value

# define map function
map_fun = '''function(doc) {
	for (msg in doc.msgs) {
		emit(doc.msgs[msg].timestamp, doc.msgs[msg].message);
	}
}'''

couch = couchdb.Server('http://' + getip.get_ip_address('wlan0') + ':5984')		# connect to server

if 'fsb-test' in couch:
	db = couch['fsb-test']		# get database
else:
	db = couch.create('fsb-test')	# or create new database

print "Content-Type: text/html\n\n"

print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">'
print '<HTML>'
print '<HEAD>'
print '	<META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=utf-8">'
print '	<TITLE></TITLE>'
print '	<meta name="generator" content="Bluefish 2.0.1" >'
print '	<meta name="author" content="James P. Valleroy" >'
print '	<META NAME="CREATED" CONTENT="20100906;18311700">'
print '	<META NAME="CHANGEDBY" CONTENT="James Valleroy">'
print '	<META NAME="CHANGED" CONTENT="20100906;18410500">'
print '	<META NAME="CHANGEDBY" CONTENT="James Valleroy">'
print '	<STYLE TYPE="text/css">'
print '	<!--'
print '		H4.cjk { font-family: "WenQuanYi Zen Hei" }'
print '		H4.ctl { font-family: "Lohit Devanagari" }'
print '		H2.cjk { font-family: "WenQuanYi Zen Hei" }'
print '		H2.ctl { font-family: "Lohit Devanagari" }'
print '	-->'
print '	</STYLE>'
print '</HEAD>'
print '<BODY LANG="en-US" DIR="LTR">'
print '<H1><A HREF="index-render.py">Free Speech Board</A></H1>'
print '<H4 CLASS="western"><I>You are on Node #1. (<A HREF="about-render.py">More'
print 'Information</A>)</I></H4>'
print '<H4 CLASS="western"><A HREF="index-render.py">Back to List of'
print 'Topics</A></H4>'

if 'page' in form:
	topicPage = int(form['page'].value)
else:
	topicPage = 1

print '<H2 CLASS="western">Topic: '
print db[topicid]['subject']
print '</H2>'
print '<TABLE WIDTH=683 BORDER=0 CELLPADDING=4 CELLSPACING=0>'
print '	<COL WIDTH=160>'
print '	<COL WIDTH=507>'
print '	<TR VALIGN=TOP>'
print '		<TH WIDTH=160>'
print '			<P>Time</P>'
print '		</TH>'
print '		<TH WIDTH=507>'
print '			<P>Message</P>'
print '		</TH>'
print '	</TR>'

# Print messages
msgNum = 0
for row in db.query(map_fun, descending=False):
#for msg in db[topicid]['msgs']:
	if row.id == topicid:
	#if 'message' in db[topicid]['msgs'][msg]:	# filter out _id and _rev fields
		if (msgNum >= (topicPage-1)*10) and (msgNum <= (topicPage*10)-1):
			print '	<TR VALIGN=TOP>'
			print '		<TD WIDTH=160 SDVAL="40427" SDNUM="1033;0;MM/DD/YY HH:MM AM/PM">'
			print '			<P ALIGN=CENTER>'
			#print time.asctime(time.localtime(db[topicid]['msgs'][msg]['timestamp']))
			print time.asctime(time.localtime(row.key))
			print '</P>'
			print '		</TD>'
			print '		<TD WIDTH=507>'
			print '			<P>'
			#print db[topicid]['msgs'][msg]['message']
			print row.value
			print '			</P>'
			print '		</TD>'
			print '	</TR>'
		msgNum = msgNum + 1

print '</TABLE>'
print '<form action = "addmsg.py" method = "get">'
print '  Message:</br>'
print '  <textarea name="'
print topicid
print '" cols=60 rows=6></textarea></br>'
print '  <input type="submit" value="Submit" />'
print '</form>'
print '<P><BR><BR>'
print '</P>'

print '<H4 CLASS="western"><I><A HREF="topic-render.py?page='
print topicPage + 1
print '&topicid='
print topicid
print '">Show next 10 messages</A></I></H4>'
print '<H4 CLASS="western"><A HREF="index-render.py">Back to List of'
print 'Topics</A></H4>'
print '</BODY>'
print '</HTML>'

