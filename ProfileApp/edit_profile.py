#!/usr/bin/python3
"""
Shows the current user profile edit details page and save edited information in database.
"""
import cgi
import cgitb
import configparser
import os

from connection import execute
from model import Employee, BaseClass
from session import Session
from utils import get_formvalues, save_uploaded_file

cgitb.enable()
config = configparser.ConfigParser()
config.read('constants.cnf')
session = Session()
employee_id = session.current_user()
header = dict()
header["title"] = "Edit Profile"
header["css_version"] = config.get("version", "css")
footer = {
    "js_version": config.get("version", "css")
}
if employee_id:
    header["homeUrl"] = "http://localhost/profiles.py"
    user = execute(BaseClass.user_name(employee_id))["fetchall"][0]
    user_name = user["firstName"] + ' ' + user["lastName"]
    top_right_link = '<a href="http://localhost/logout.py">Logout</a>'
    header["navTopRight"] = '<li class="active"><a>%s</a></li><li class="active">%s</li>' % (user_name, top_right_link)
    if os.environ['REQUEST_METHOD'] == 'GET':
        form = cgi.FieldStorage()
        employee_query = execute(["SELECT firstName, lastName, email, dob, image_extension, preferCommun, prefix,"
                                  " maritalStatus, employer,employment FROM employee WHERE id=%s",
                                  (str(employee_id),)])["fetchall"][0]
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
        print("Content-type: text/html\n")
        f = open('./template/header.html', encoding='utf-8')
        print(f.read() % header)
        f.close()
        f = open('./template/edit_profile.html')
        print(f.read() % employee_columns)
        f.close()
        f = open('./template/footer.html', encoding="utf_8")
        print(f.read() % footer)
        f.close()

    elif os.environ['REQUEST_METHOD'] == 'POST':
        dict_fields = get_formvalues()
        e = Employee(dict_fields)
        employee_id = str(employee_id)
        update_query = e.update_employee(employee_id)
        execute(update_query)
        if dict_fields['photo'].filename:
            image_ext = dict_fields['photo'].filename.split('.')[-1]
            image_name = employee_id + '.' + image_ext
            image_query = e.set_image(image_ext, employee_id)
            execute(image_query)
            save_uploaded_file(dict_fields['photo'], config.get('profile', 'path'), image_name)
        print("Location: http://localhost/edit_profile.py\n")
else:
    print("Location: http://localhost/login.py\n")
