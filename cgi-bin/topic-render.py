#!/usr/bin/python

import time
import couchdb

couch = couchdb.Server()		# connect to server

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

for thread in db:
	print '<H2 CLASS="western">Topic: I like cats</H2>'
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
	for msg in db[thread]:
		if 'message' in db[thread][msg]:	# filter out _id and _rev fields
			print '	<TR VALIGN=TOP>'
			print '		<TD WIDTH=160 SDVAL="40427" SDNUM="1033;0;MM/DD/YY HH:MM AM/PM">'
			print '			<P ALIGN=CENTER>'
			print time.asctime(time.localtime(db[thread][msg]['timestamp']))
			print '</P>'
			print '		</TD>'
			print '		<TD WIDTH=507>'
			print '			<P>'
			print db[thread][msg]['message']
			print '			</P>'
			print '		</TD>'
			print '	</TR>'

	print '</TABLE>'
	print '<form action = "addmsg.py" method = "get">'
	print '  Message:</br>'
	print '  <textarea name="newmsg" cols=60 rows=6></textarea></br>'
	print '  <input type="submit" value="Submit" />'
	print '</form>'
	print '<P><BR><BR>'
	print '</P>'

print '<H4 CLASS="western"><I><A HREF="../fsb">Show next 100 messages</A>'
print '</I><SPAN STYLE="font-style: normal"><SPAN STYLE="font-weight: normal"><SPAN STYLE="background: #ffff00">(only'
print 'shown when applicable)</SPAN></SPAN></SPAN></H4>'
print '<H4 CLASS="western"><A HREF="index-render.py">Back to List of'
print 'Topics</A></H4>'
print '</BODY>'
print '</HTML>'

