#!/usr/bin/python3
from connection import execute
from model import BaseClass

import os
import json
import configparser


config = configparser.ConfigParser()
config.read('constants.cnf')
if os.environ['REQUEST_METHOD'] == 'GET':
    user_data = execute(BaseClass.user_profile_data())["fetchall"]
    for i in range(len(user_data)):
        user_data[i]["image_extension"] = '<img src="%s" class="img-responsive img-thumbnail profile-img " ' \
                                          'alt="Profile Image">' % (config.get('profile', 'img_path') + str(user_data[i]["id"]) + '.' + user_data[i]["image_extension"])
    print("Content-type: text/html\n")
    print(json.dumps(user_data))
