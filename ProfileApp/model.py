#!/usr/bin/python3
import re


class BaseClass:
    @staticmethod
    def select_all(user):
        return ["SELECT * FROM employee WHERE id=%s", (user,)]

    @staticmethod
    def update_user_setting(values, id):
        query = ["UPDATE employee SET password = %s, public_profile = %s WHERE id=%s",
                 (values["password"], values["profile_status"], id,)]
        return query

    @staticmethod
    def user_profile_data(page):
        offset = int(page) * 10
        query = ["SELECT id,firstName, lastName, image_extension, email, employer, employment FROM employee "
                 "WHERE public_profile = 1 LIMIT 10 OFFSET %s", (offset,)]
        return query


class Employee:
    def __init__(self, employee):
        self.first_name = employee['firstName']
        self.last_name = employee['lastName']
        self.email = employee['email']
        self.dob = employee['dob']
        if 'photo' in employee:
            self.image = employee['photo']
        else:
            self.image = 'NULL'
        self.prefix = employee['prefix']
        self.employment = employee['employment']
        self.employer = employee['employer']
        self.marital_status = employee['maritalStatus']
        self.prefer_commun = employee['communication']

    def validation(self):
        self.flag = True
        if not re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", self.email):
            print("Validation issue with email")
            self.flag = False
        if not re.match("^[a-zA-Z]{2,30}$", self.first_name):
            print("Validation issue with First Name")
            self.flag = False
        if not re.match("^[a-zA-Z]{2,30}$", self.last_name):
            print("Validation issue with Last Name")
            self.flag = False
        if not re.match("^[a-zA-Z]{2,30}$", self.employer):
            print("Validation issue with Employer")
            self.flag = False
        if not re.match("^[a-zA-Z]{2,30}$", self.employment):
            print("Validation issue with Employment")
            self.flag = False
        if (len(self.image.filename.split('.')) > 1 and
                (self.image.filename.split('.')[-1].upper() not in ["GIF", "PNG", "JPG", "JPEG"])):
            print("Validation issue with Image")
            self.flag = False

        return self.flag

    def select_employee(self, *args):
        self.query = "SELECT {} FROM employee".format(','.join(args))
        return self.query

    def delete_employee(self, id):
        """
        This function create delete query.
        :param id: id of the field which needs to be deleted
        :return: delete query
        """
        self.query = "DELETE FROM employee WHERE ID=%s" % id
        return self.query

    def insert_employee(self):
        """
        This function create update query for employee table
        :return: insert query
        """
        if self.validation():
            return ["INSERT INTO employee (firstName,lastName,email, dob, prefix, employment, employer, " \
                    "maritalStatus, preferCommun)" \
                    "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (self.first_name, self.last_name, self.email, self.dob,
                     self.prefix, self.employment, self.employer, self.marital_status, self.prefer_commun,)]
        else:
            raise ValueError('Some fields failed validation.')

    def update_employee(self, id):
        """
        This function create insert query for employee table
        :return: insert query
        """
        if self.validation():
            return ["UPDATE employee SET firstName=%s,lastName=%s,email=%s, dob=%s, prefix=%s, " \
                    "employment=%s, employer=%s, maritalStatus=%s, preferCommun=%s WHERE id=%s"
                , (self.first_name, self.last_name, self.email, self.dob, self.prefix, self.employment,
                   self.employer, self.marital_status, self.prefer_commun, id,)]
        else:
            raise ValueError('Some fields failed validation.')

    @staticmethod
    def set_image(image_ext, id):
        return ["UPDATE employee SET image_extension=%s WHERE id=%s", (image_ext, id,)]


class EmployeeAddress:
    def __init__(self, employee):
        self.street = employee['homeStreet']
        self.city = employee['homeCity']
        self.state = employee['homeState']
        self.pin = employee['homePin']
        self.phone = employee['homePhone']
        self.fax = employee['homeFax']
