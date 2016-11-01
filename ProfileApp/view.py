#!/usr/bin/python3

import os
import cgi
import cgitb
from model import Employee
from connection import execute
import shutil

cgitb.enable()



def get_formvalues():
    """
    This function is used to create dictionary for all the fields on Form.
    """
    form = cgi.FieldStorage()
    dict_fields = {}
    for i in form:
        if str(i) == 'photo':
            dict_fields[str(i)] = form[str(i)]
        else:
            dict_fields[str(i)] = form.getvalue(str(i))
    return dict_fields


def save_uploaded_file(fileitem, upload_dir, image_name):
    print('Inside save image')
    outpath = os.path.join(upload_dir, image_name)
    # print('4')
    # print(str(outpath))
    with open(outpath, 'wb') as fout:
        shutil.copyfileobj(fileitem.file, fout, 100000)

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
    # execute(insert_query)
    last_id = execute(insert_query)
    image_name = str(last_id)+'.'+dict_fields['photo'].filename.split('.')[-1]
    image_query = "UPDATE employee SET image='%s' where id=%s" % (image_name, str(last_id))
    print("Last id:", last_id)
    # print(dict_fields)
    execute(image_query)
    f = open('./template/login.html')
    print(f.read())
    f.close()
    print('End')
    save_uploaded_file(dict_fields['photo'], '/var/www/html/Details/ProfileApp/static/profile_images/', image_name)
