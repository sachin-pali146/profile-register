#!/usr/bin/python3

import cgi
import cgitb
import shutil
import os
import smtplib
import hashlib
import string
import random
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser

config = configparser.ConfigParser()
config.read('constants.cnf')
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


def send_email(user_email,activation):
    try:
        msg = MIMEMultipart()
        msg['Subject'] = "Activate your account"
        msg['From'] = config.get('smtp', 'user')
        msg['To'] = user_email
        msg.preamble = 'body'
        template = open('./template/email_template.txt')
        body = MIMEText(template.read() % activation, 'html')
        template.close()
        msg.attach(body)
        
        # Send the message via our own SMTP server.

        server = smtplib.SMTP(config.get('smtp', 'host'), config.get('smtp', 'port'))
        server.ehlo()
        server.starttls()
        server.login(config.get('smtp', 'user'), config.get('smtp', 'pass'))
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(e)


def generate_password():
    special = '!@#$%^&*'
    password = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase+special) for _ in range(10))
    matcher = re.compile(r'^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[!@#\$%\^&\*])[A-Za-z\d!@#\$%\^&\*]{8,}$')
    if matcher.match(password):
        return password
    else:
        while not matcher.match(password):
            password = generate_password()
        return password


def generate_hash(input_value):
    return hashlib.new('ripemd160', str(input_value).encode()).hexdigest()
