#!/usr/bin/python3
import re
from utils import generate_hash,generate_password


class BaseClass(object):

    def insert(self, dict_value):
        columns = []
        values = []
        for key, value in dict_value.items():
            columns.append(key)
            values.append(value)
        values = tuple(values)
        query = "INSERT INTO %s (" % self.name + ", ".join(columns) + ") VALUES(" + ", ".join(["%s"]*len(columns)) + ")"
        return [query, values]

    def select(self, columns, condition=None):
        print(self.name)
        query = "SELECT %s from %s"

        if condition:
            query += " WHERE %s"
        return [query, (', '.join(columns), self.name, condition,)]

    def update(self, column_dict, condition):
        query = "UPDATE %s SET " % self.name
        columns = []
        values = []
        for key, value in column_dict.items():
            columns.append("%s = " % key + "%s")
            values.append(value)
        query += ', '.join(columns)

        if condition:
            query += " WHERE %s"
            values += condition
        values = tuple(values)

        return [query, values]

    def delete(self, condition):
        query = "DELETE FROM %s"

        if condition:
            query += " WHERE %s"
        return [query, (self.name, condition,)]

    @staticmethod
    def select_all(user):

        """
        Returns SQL query array having all the columns for given user
        :param user: user id of the user whose details needed to be fetched
        :return: SQL query array
        """

        return ["SELECT * FROM employee WHERE id=%s", (user,)]

    @staticmethod
    def update_user_setting(values, id):

        """
        Returns Update query for values of user settings
        :param values: dictionary having password and public profile information
        :param id: User id
        :return: SQL query array
        """

        query = ["UPDATE employee SET password = %s, public_profile = %s WHERE id=%s",
                 (values["password"], values["profile_status"], id,)]
        return query

    @staticmethod
    def user_profile_data(page):

        """
        Return Query having details of public profiles
        :param page: page number of user profile list
        :return: SQL query array
        """

        offset = int(page) * 10
        query = ["SELECT SQL_CALC_FOUND_ROWS id,firstName, lastName, image_extension, email, employer, employment "
                 "FROM employee WHERE public_profile = 1 LIMIT 10 OFFSET %s", (offset,)]
        return query


class Employee(BaseClass):
    name = 'employee'

    def __init__(self, employee):

        """
        Initialise employee class.
        :param employee: dictionary having basic employee details
        """

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
        self.password = generate_password()

    def validation(self):

        """
        Validate the information sent by user.
        :return: Boolean value according to validation test.
        """

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

    def insert_employee(self):
        """
        This function create update query for employee table
        :return: insert query
        """
        if self.validation():
            columns={
                'firstName':self.first_name,
                'lastName':self.last_name,
                'email':self.email,
                'dob': self.dob,
                'prefix':self.prefix,
                'employment':self.employment,
                'employer':self.employer,
                'maritalStatus':self.marital_status,
                'preferCommun':self.prefer_commun
            }
            return self.insert(columns)
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

    def activation(self):

        """
        Create activation details new registered users
        :return: dictionary having activation url and password.
        """

        hash_value = generate_hash(self.email)
        activation_url = "http://localhost/activate.py?email=%s&value=%s" % (self.email, hash_value)
        result = dict()
        result['activation_url'] = activation_url
        result['temp_password'] = self.password
        result['user_name'] = ' '.join([self.first_name, self.last_name])
        return result

    @staticmethod
    def set_image(image_ext, id):
        """
        Sets user profile image
        :param image_ext: profile image extension
        :param id: user id
        :return: SQL query array
        """
        return ["UPDATE employee SET image_extension=%s WHERE id=%s", (image_ext, id,)]


class EmployeeAddress(BaseClass):
    def __init__(self, employee):
        self.name = 'empAddress'
        self.street = employee['homeStreet']
        self.city = employee['homeCity']
        self.state = employee['homeState']
        self.pin = employee['homePin']
        self.phone = employee['homePhone']
        self.fax = employee['homeFax']
