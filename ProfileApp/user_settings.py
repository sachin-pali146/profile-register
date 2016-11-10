#!/usr/bin/python3
"""
Create User settings page from where they can change their password and make their profile public.
"""
import cgi
import cgitb
import os

from connection import execute
from model import BaseClass
from session import current_user

cgitb.enable()
form = cgi.FieldStorage()
user = str(current_user())

if user:
    if os.environ['REQUEST_METHOD'] == 'GET':
        print("Content-type: text/html")
        print('')
        f = open('./template/header.html')
        print(f.read() % {'title': 'User Settings'})
        f.close()
        f = open('./template/user_settings.html')
        print(f.read())
        f.close()
        f = open('./template/footer.html')
        print(f.read())
        f.close()
    elif os.environ['REQUEST_METHOD'] == 'POST':
        u = BaseClass
        user_values = execute(u.select_all(user))["fetchall"][0]
        old_password = form.getvalue('oldPassword')
        new_password = form.getvalue('newPassword')
        confirm_password = form.getvalue('confirmPassword')
        if 'profileStatus' in form.keys():
            profile_status = True
        else:
            profile_status = False

        if new_password == confirm_password:
            if old_password == user_values["password"]:
                updated_values = dict()
                updated_values["password"] = new_password
                updated_values["profile_status"] = profile_status
                execute(u.update_user_setting(updated_values, user))
                print("Location: http://localhost/user_settings.py\n")
            else:
                print("Content-type: text/html\n")
                print("You entered wrong current password")
        else:
            print("Content-type: text/html\n")
            print("Your passwords does not match")

else:
    print("Location: http://localhost/login.py\n")
