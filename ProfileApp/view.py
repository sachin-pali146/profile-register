#!/usr/bin/python3

import os
import configparser

from model import Employee
from connection import execute
from utils import get_formvalues, save_uploaded_file

config = configparser.ConfigParser()
config.read('constants.cnf')

if os.environ['REQUEST_METHOD'] == 'GET':
    print("Content-type: text/html")
    print('')
    f = open('./template/index.html')
    print(f.read())
    f.close()
elif os.environ['REQUEST_METHOD'] == 'POST':
    print("Content-type:text/html\r\n\r\n")
    dict_fields = get_formvalues()
    e = Employee(dict_fields)
    insert_query = e.insert_employee()
    last_id = execute(insert_query)["lastrowid"]
    if dict_fields['photo'].filename:
        image_ext = dict_fields['photo'].filename.split('.')[-1]
        image_name = str(last_id)+'.'+image_ext
        image_query = e.set_image(image_ext, str(last_id))
        execute(image_query)
        save_uploaded_file(dict_fields['photo'], config.get('profile', 'path'), image_name)
    f = open('./template/login.html')
    print(f.read())
    f.close()

