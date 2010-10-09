#!/usr/bin/python

import time
import couchdb

# define map function
map_fun = '''function(doc) {
	emit(doc.updatetime, [doc.subject, doc.createtime, doc.updatetime, doc.msgs])
}'''

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
print '	<META NAME="GENERATOR" CONTENT="OpenOffice.org 3.2  (Unix)">'
print '	<META NAME="AUTHOR" CONTENT="James Valleroy">'
print '	<META NAME="CREATED" CONTENT="20100906;15445800">'
print '	<META NAME="CHANGEDBY" CONTENT="James Valleroy">'
print '	<META NAME="CHANGED" CONTENT="20100906;18403900">'
print '	<META NAME="CHANGEDBY" CONTENT="James Valleroy">'
print '	<STYLE TYPE="text/css">'
print '	<!--'
print '		H2.cjk { font-family: "WenQuanYi Zen Hei" }'
print '		H2.ctl { font-family: "Lohit Devanagari" }'
print '		H4.cjk { font-family: "WenQuanYi Zen Hei" }'
print '		H4.ctl { font-family: "Lohit Devanagari" }'
print '	-->'
print '	</STYLE>'
print '</HEAD>'
print '<BODY LANG="en-US" DIR="LTR">'
print '<H1>Free Speech Board</H1>'
print '<H4 CLASS="western"><I>You are on Node #1. (<A HREF="about-render.py">More'
print 'Information</A>)</I></H4>'
print '<H2 CLASS="western">Topics</H2>'
print '<TABLE WIDTH=884 BORDER=0 CELLPADDING=0 CELLSPACING=0>'
print '	<COL WIDTH=24>'
print '	<COL WIDTH=380>'
print '	<COL WIDTH=176>'
print '	<COL WIDTH=168>'
print '	<COL WIDTH=136>'
print '	<TR VALIGN=TOP>'
print '		<TH WIDTH=24>'
print '			<P><BR>'
print '			</P>'
print '		</TH>'
print '		<TH WIDTH=380>'
print '			<P>Topic</P>'
print '		</TH>'
print '		<TH WIDTH=176>'
print '			<P>Started</P>'
print '		</TH>'
print '		<TH WIDTH=168>'
print '			<P>Last Update</P>'
print '		</TH>'
print '		<TH WIDTH=136>'
print '			<P>Number of Posts</P>'
print '		</TH>'
print '	</TR>'

# get rows (represent docs) sorted by updatetime
for row in db.query(map_fun, descending=True):
	print '	<TR VALIGN=TOP>'
	print '		<TD WIDTH=24 SDVAL="1" SDNUM="1033;">'
	print '			<P>1</P>'
	print '		</TD>'
	print '		<TD WIDTH=380>'
	print '			<P><A HREF="topic-render.py">'
	print row.value[0]
	print '			</A></P>'
	print '		</TD>'
	print '		<TD WIDTH=176 SDVAL="40427" SDNUM="1033;0;MM/DD/YY HH:MM AM/PM">'
	print '			<P ALIGN=CENTER>'
	print time.asctime(time.localtime(row.value[1]))
	print '			</P>'
	print '		</TD>'
	print '		<TD WIDTH=168 SDVAL="40427" SDNUM="1033;0;MM/DD/YY HH:MM AM/PM">'
	print '			<P ALIGN=CENTER>'
	print time.asctime(time.localtime(row.value[2]))
	print '			</P>'
	print '		</TD>'
	print '		<TD WIDTH=136 SDVAL="5" SDNUM="1033;">'
	print '			<P ALIGN=CENTER>'
	print len(row.value[3])
	print '			</P>'
	print '		</TD>'
	print '	</TR>'

print '</TABLE>'
print '<H4 CLASS="western"><I><A HREF="../fsb">Show next 100 topics</A></I></H4>'
print '<FORM ACTION="addtopic.py">'
print '	<H2 CLASS="western">Create New Topic:<BR><TEXTAREA NAME="newtopic" ROWS=2 COLS=32 STYLE="width: 2.83in; height: 0.66in"></TEXTAREA><BR><INPUT TYPE=SUBMIT VALUE="Submit" STYLE="width: 0.84in; height: 0.37in">'
print '		</H2>'
print '</FORM>'
print '<P><BR><BR>'
print '</P>'
print '</BODY>'
print '</HTML>'
