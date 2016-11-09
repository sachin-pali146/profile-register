#!/usr/bin/python3

import cgi
import json
import os


form = cgi.FieldStorage()
profile_file = form.getvalue("profile")
values = dict()
print("Content-type: text/html\n")

for line in profile_file.split(',\n'):
    line = line.split(',')
    if line[0]=='First Name':
        values["firstName"]=line[1]
    elif line[0]=="Last Name":
        values["lastName"]=line[1]
    elif line[0]=="DOB":
        values["dob"]=line[1]
    elif line[0]=="email":
        values["email"]=line[1]
    elif line[0]=="Marital Status":
        values["maritalStatus"]=line[1]
    elif line[0]=="Employer":
        values["employer"]=line[1]
    elif line[0]=="Employment":
        values["employment"]=line[1]

if os.environ['REQUEST_METHOD'] == 'POST':
    print(json.dumps(values))
