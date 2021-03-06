#!/usr/bin/python3
"""
Have all the utility functions used in profile app.
"""
import cgi
import cgitb
import configparser
import datetime
import hashlib
import os
import random
import re
import shutil
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# from model import BaseClass
# from session import Session


def create_log(error_log):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_name = str(datetime.date.today()) + '.txt'
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    error_log = str(timestamp) + " : " + str(error_log) + '\n'
    log_file = open(os.path.join('logs', file_name), 'a')
    log_file.write(error_log)
    log_file.close()

try:

    config = configparser.ConfigParser()
    config.read('constants.cnf')
    cgitb.enable()
    # session = Session()
    # employee_id = session.current_user()
    header = dict()


    def show_404():
        pass
    #     header["title"] = "Error"
    #     header["css_version"] = config.get("version", "css")
    #     footer = {
    #         "js_version": config.get("version", "css")
    #     }
    #     if employee_id:
    #         from connection import execute
    #
    #         header["homeUrl"] = "http://localhost/profiles.py"
    #         user = execute(BaseClass.user_name(employee_id))["fetchall"][0]
    #         user_name = user["firstName"] + ' ' + user["lastName"]
    #         top_right_link = '<a href="http://localhost/logout.py">Logout</a>'
    #         header["navTopRight"] = '<li class="active"><a>%s</a></li><li class="active">%s</li>' % (
    #             user_name, top_right_link)
    #     else:
    #         header["homeUrl"] = "http://localhost/register.py"
    #         header["navTopRight"] = '<li class="active"><a href="http://localhost/register.py">Register Now</a></li>'
    #
    #     print("Content-type: text/html")
    #     print('')
    #     f = open('./template/header.html')
    #     print(f.read() % header)
    #     f.close()
    #     f = open('./template/404.html')
    #     print(f.read())
    #     f.close()
    #     f = open('./template/footer.html')
    #     print(f.read() % footer)
    #     f.close()

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


    def send_email(user_email, activation):
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
        password = ''.join(
            random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase + special) for _ in range(10))
        matcher = re.compile(r'^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[!@#\$%\^&\*])[A-Za-z\d!@#\$%\^&\*]{8,}$')
        if matcher.match(password):
            return password
        else:
            while not matcher.match(password):
                password = generate_password()
            return password


    def generate_hash(input_value):
        return hashlib.new('ripemd160', str(input_value).encode()).hexdigest()
except Exception as e:
    create_log("Utils.py : "+str(e))
