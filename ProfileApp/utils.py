#!/usr/bin/python3

import cgi
import cgitb
import shutil
import os

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

    """
    Create a copy of profile image on server.
    :param fileitem: uploaded file object
    :param upload_dir: server upload path
    :param image_name: name for image file.
    """

    outpath = os.path.join(upload_dir, image_name)
    with open(outpath, 'wb') as fout:
        shutil.copyfileobj(fileitem.file, fout, 100000)
