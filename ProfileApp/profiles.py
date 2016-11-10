#!/usr/bin/python3
"""
Displays all the Public profiles
"""
import configparser
import os

from connection import execute
from model import BaseClass
from session import current_user

config = configparser.ConfigParser()
config.read('constants.cnf')
employee_id = current_user()
header = dict()
header["title"] = "Edit Profile"

if employee_id:
    header["homeUrl"] = "http://localhost/profiles.py"
    user = execute(BaseClass.user_name(employee_id))["fetchall"][0]
    user_name = user["firstName"] + ' ' + user["lastName"]
    top_right_link = '<a href="http://localhost/logout.py">Logout</a>'
    header["navTopRight"] = '<li class="active"><a>%s</a></li><li class="active">%s</li>' % (user_name, top_right_link)
    header["css_version"] = config.get("version", "css")
    footer = {
        "js_version": config.get("version", "css")
    }
    if os.environ['REQUEST_METHOD'] == 'GET':
        print("Content-type: text/html\n")
        f = open('./template/header.html', encoding='utf-8')
        print(f.read() % header)
        f.close()
        f = open('./template/profiles.html')
        print(f.read())
        f.close()
        f = open('./template/footer.html', encoding="utf_8")
        print(f.read() % footer)
        f.close()
else:
    print("Location: http://localhost/login.py\n")
