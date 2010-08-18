#!/usr/bin/python
""" addmsg.py
responds to askName.html
and gives a customized greeting
"""
import cgi

print "Content-type: text/html \n\n"

form = cgi.FieldStorage()
userName = form["userName"].value
print "<h1>Hi there, %s!</h1>" % userName

