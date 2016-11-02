#!/usr/bin/python

# Import modules for CGI handling 
import cgi

import mysql.connector
from mysql.connector import Error


form = cgi.FieldStorage()

print("Content-type:text/html\r\n\r\n")
print('<html>')
print('<head>')
print('<title>Form Submission Complete</title>')
print('</head>')
print('<body>')
for i in form:
    print('<h2>' + str(i) + '</h2>')
print('</body>')
print('</html>')
print(form)
# Get data from fields
prefix = form.getvalue('prefix')
firstName = form.getvalue('firstName')
lastName = form.getvalue('lastName')
photo = form.getvalue('photo')
dob = form.getvalue('dob')
employment = form.getvalue('employment')
employer = form.getvalue('employer')
communication = form.getvalue('communication')
homeStreet = form.getvalue('homeStreet')
homeCity = form.getvalue('homeCity')
homeState = form.getvalue('homeState')
homePin = form.getvalue('homePin')
homePhone = form.getvalue('homePhone')
homeFax = form.getvalue('homeFax')
officeStreet = form.getvalue('officeStreet')
officeCity = form.getvalue('officeCity')
officeState = form.getvalue('officeState')
officePin = form.getvalue('officePin')
officePhone = form.getvalue('officePhone')
officeFax = form.getvalue('officeFax')
maritalStatus = form.getvalue('maritalStatus')
checkbox_address = form.getvalue('checkboxAddress')

print(checkbox_address)


def connect():
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='profiledb',
                                       user='root',
                                       password='mindfire')
        if conn.is_connected():
            print('Connected to MySQL database')
            add_employee = ("INSERT INTO employee"
                            "(maritalStatus,firstName,dob,lastName,employer,prefix,preferCommun,employment)"
                            "VALUES (%(maritalStatus)s, %(firstName)s, %(dob)s, %(lastName)s, %(employer)s, %(prefix)s,"
                            " %(communication)s, %(employment)s)")
            data_employee = {
                'maritalStatus': maritalStatus,
                'firstName': firstName,
                'dob': dob,
                'lastName': lastName,
                'employer': employer,
                'prefix': prefix,
                'communication': communication,
                'employment': employment
            }
            cursor = conn.cursor()
            cursor.execute(add_employee, data_employee)

            if cursor.lastrowid:
                last_empid = cursor.lastrowid
            else:
                last_empid = None

            conn.commit()
            print(checkbox_address == 'sameAddress', checkbox_address)

            if checkbox_address == 'sameAddress':
                address_type = 'both'
                add_address = ("INSERT INTO empAddress"
                               "(empID,type,state,fax,street,city,pin,phone) "
                               "VALUES (%(empID)s, %(type)s,%(homeState)s, %(homeFax)s, %(homeStreet)s, %(homeCity)s,"
                               " %(homePin)s, %(homePhone)s)")
                data_address = {
                    'empID': last_empid,
                    'type': address_type,
                    'homeState': homeState,
                    'homeFax': homeFax,
                    'homeStreet': homeStreet,
                    'homeCity': homeCity,
                    'homePin': homePin,
                    'homePhone': homePhone
                }
                cursor = conn.cursor()
                cursor.execute(add_address, data_address)
            else:
                address_type = 'home'
                add_address = ("INSERT INTO empAddress"
                               "(empID,type,state,fax,street,city,pin,phone) "
                               "VALUES (%(empID)s, %(type)s,%(homeState)s, %(homeFax)s, %(homeStreet)s, %(homeCity)s,"
                               " %(homePin)s, %(homePhone)s)")
                data_address = {
                    'empID': last_empid,
                    'type': address_type,
                    'homeState': homeState,
                    'homeFax': homeFax,
                    'homeStreet': homeStreet,
                    'homeCity': homeCity,
                    'homePin': homePin,
                    'homePhone': homePhone
                }
                cursor = conn.cursor()
                cursor.execute(add_address, data_address)

                address_type = 'office'
                add_address = ("INSERT INTO empAddress"
                               "(empID,type,state,fax,street,city,pin,phone) "
                               "VALUES (%(empID)s, %(type)s,%(officeState)s, %(officeFax)s, %(officeStreet)s,"
                               " %(officeCity)s, %(officePin)s, %(officePhone)s)")
                data_address = {
                    'empID': last_empid,
                    'type': address_type,
                    'officeState': officeState,
                    'officeFax': officeFax,
                    'officeStreet': officeStreet,
                    'officeCity': officeCity,
                    'officePin': officePin,
                    'officePhone': officePhone
                }
                cursor.execute(add_address, data_address)

            conn.commit()

    except Error as e:
        print(e)

    finally:
        conn.close()


connect()