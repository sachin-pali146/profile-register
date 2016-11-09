#!/usr/bin/python3

import cgi
import json
import os

form = cgi.FieldStorage()
profile_file = form.getvalue("profile")
values = dict()
print("Content-type: text/html\n")
# print(profile_file)
valid_values = {
    "First Name": "firstName",
    "Last Name": "lastName",
    "DOB": "dob",
    "email": "email",
    "Employment": "employment",
    "Employer": "employer",
    "Home Street": "homeStreet",
    "Home City": "homeCity",
    "Home State": "homeState",
    "Home Pin": "homePin",
    "Home Phone": "homePhone",
    "Home Fax": "homeFax",
    "Office Street": "officeStreet",
    "Office City": "officeCity",
    "Office State": "officeState",
    "Office Pin": "officePin",
    "Office Phone": "officePhone",
    "Office Fax": "officeFax"
}
for line in profile_file.split('\n'):
    line = line.split(',')
    if line[0] in valid_values.keys():
        values[valid_values[line[0]]] = line[1]

if os.environ['REQUEST_METHOD'] == 'POST':
    print(json.dumps(values))
