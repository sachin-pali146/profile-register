#!/usr/bin/python3

import os
import cgi
import cgitb
import configparser

from session import current_user
from model import Employee
from connection import execute
from utils import get_formvalues, save_uploaded_file


cgitb.enable()
config = configparser.ConfigParser()
config.read('constants.cnf')
employee_id = current_user()

if employee_id:
    if os.environ['REQUEST_METHOD'] == 'GET':
        form = cgi.FieldStorage()
        employee_query = execute(["SELECT firstName, lastName, email, dob, image_extension, preferCommun, prefix,"
                                 " maritalStatus, employer,employment FROM employee where id=%s", (str(employee_id),)])["fetchall"][0]
        employee_columns = {
            "firstName": employee_query["firstName"],
            "lastName": employee_query["lastName"],
            "email": employee_query["email"],
            "dob": employee_query["dob"],
            "image": './static/profile_images/' + str(employee_id) + '.' + employee_query["image_extension"],
            "preferCommun": employee_query["preferCommun"],
            "prefix": employee_query["prefix"],
            "maritalStatus": employee_query["maritalStatus"],
            "employer": employee_query["employer"],
            "employment": employee_query["employment"],
            "employee_id": str(employee_id),
            "master": "",
            "miss": "",
            "mr": "",
            "mrs": "",
            "Phone": "",
            "Mail": "",
            "married": "",
            "unmarried": ""
        }
        employee_columns[employee_columns["preferCommun"]] = "selected"
        employee_columns[employee_columns["prefix"]] = "selected"
        employee_columns[employee_columns["maritalStatus"]] = "selected"
        print("Content-type: text/html")
        print('')
        f = open('./template/header.html')
        print(f.read() % {'title': 'Edit Profile'})
        f.close()
        f = open('./template/edit_profile.html')
        print(f.read() % employee_columns)
        f.close()
        f = open('./template/footer.html')
        print(f.read())
        f.close()

    elif os.environ['REQUEST_METHOD'] == 'POST':
        # print("Content-type: text/html\n")
        dict_fields = get_formvalues()
        # print('1',dict_fields)
        e = Employee(dict_fields)
        # print('2')
        employee_id = str(employee_id)
        update_query = e.update_employee(employee_id)
        # print('4')
        execute(update_query)
        # print('5')
        # print(update_query)
        if dict_fields['photo'].filename:
            # print('3')
            image_ext = dict_fields['photo'].filename.split('.')[-1]
            image_name = employee_id+'.'+image_ext
            image_query = e.set_image(image_ext, employee_id)
            execute(image_query)
            save_uploaded_file(dict_fields['photo'], config.get('profile', 'path'), image_name)
        print("Location: http://localhost/edit_profile.py\n")
else:
    print("Location: http://localhost/login.py\n")
