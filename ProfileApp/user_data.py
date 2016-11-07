#!/usr/bin/python3
from connection import execute, total_public_profile
from model import BaseClass
import cgi
import os
import json
import configparser

form = cgi.FieldStorage()
page = form.getvalue("page", 0)
config = configparser.ConfigParser()
config.read('constants.cnf')
print("Content-type: text/html\n")
if os.environ['REQUEST_METHOD'] == 'GET':
    user_query = BaseClass.user_profile_data(page)
    user_data = execute(user_query)['fetchall']
    total_user = total_public_profile()["total"]
    for i in range(len(user_data)):
        user_data[i]["image_extension"] = '<img src="%s" class="img-responsive img-thumbnail profile-img " ' \
                                          'alt="Profile Image">' % (
                                              config.get('profile', 'img_path') + str(user_data[i]["id"]) + '.' +
                                              user_data[i]["image_extension"])
    users=dict()
    users["data"]=user_data
    users["total"]=total_user
    print(json.dumps(users))
