#!/usr/bin/python

# Import the CGI module
import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()

# Print the required header that tells the browser how to render the text.
print "Content-Type: text/html\n\n"

print "<head>"
print "<meta http-equiv=\"content-type\" content=\"text/xml; charset=utf-8\" />"

print "<title>Free Speech Board</title>"
print "</head>"

print "<body>"
print "<h1>Free Speech Board</h1>"
if "newmsg" in form:
	print form["newmsg"].value
print "</br></br>"
print "<form action = \"addmsg.py\" method = \"get\">"
print "  Message:</br>"
print "  <textarea name=\"newmsg\" cols=60 rows=6></textarea></br>"
print "  <input type=\"submit\" value=\"Submit\" />"
print "</form>"
print "</body>"
print "</html>"

