#!/usr/bin/python3
"""
Return all the public profile users data in JSON format.
"""
try:
    import cgi
    import configparser
    import json
    import os

    from connection import public_profile
    from model import BaseClass
    from utils import create_log, show_404

    form = cgi.FieldStorage()
    page = form.getvalue("page", 0)
    config = configparser.ConfigParser()
    config.read('constants.cnf')
    print("Content-type: text/html\n")

    if os.environ['REQUEST_METHOD'] == 'GET':
        user_query = BaseClass.user_profile_data(page)
        user_data = public_profile(user_query)
        for i in range(len(user_data["fetchall"])):
            user_data["fetchall"][i][
                "image_extension"] = '<img src="%s" class="img-responsive img-thumbnail profile-img " ' \
                                     'alt="Profile Image">' % (
                                         config.get('profile', 'img_path') + str(
                                             user_data["fetchall"][i]["id"]) + '.' +
                                         user_data["fetchall"][i]["image_extension"])
        users = dict()
        users["data"] = user_data['fetchall']
        users["total"] = user_data["total"]
        print(json.dumps(users))
except Exception as e:
    create_log("User_data.py : "+str(e))
    show_404()
