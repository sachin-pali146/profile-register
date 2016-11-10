#!/usr/bin/python3
"""
Checks the user activation link and activate the user if it is not active.
"""
import cgi
import cgitb
import os

from connection import activate, login
from utils import generate_hash

cgitb.enable()
form = cgi.FieldStorage()
header = dict()
header["title"] = "Activate"
header["homeUrl"] = "http://localhost/register.py"
header["navTopRight"] = '<li class="active"><a href="http://localhost/register.py">Register Now</a></li>'
email = form.getvalue("email")
value = form.getvalue("value")
active = login(email)["active"]
email_hash = generate_hash(email)

if os.environ['REQUEST_METHOD'] == 'GET':
    print("Content-type: text/html\n")
    f = open('./template/header.html', encoding='utf-8')
    print(f.read() % header)
    f.close()
    if value == email_hash and not active:
        activate(email)
        print("<p>Your account has been activated. Please log in with the password assigned to you</p>")
    elif active:
        print("<p>Your account was already activated. Please log in with the password assigned to you</p>")
    else:
        print("<p>Please check your activation link</p>")
    f = open('./template/footer.html', encoding="utf_8")
    print(f.read())
    f.close()
