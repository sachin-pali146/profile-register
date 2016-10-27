#!/usr/bin/python3
import re

class Employee:
    def __init__(self, kwargs):
        self.first_name = kwargs['firstName']
        self.last_name = kwargs['lastName']
        self.email = kwargs['email']
        self.dob = kwargs['dob']
        if 'photo' in kwargs:
            self.image = kwargs['photo']
        else:
            self.image = 'NULL'
        self.prefix = kwargs['prefix']
        self.employment = kwargs['employment']
        self.employer = kwargs['employer']
        self.marital_status = kwargs['maritalStatus']
        self.prefer_commun = kwargs['communication']

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
        return self.flag

    def select_employee(self, *args):
        self.query = "SELECT {} FROM employee".format(','.join(args))
        return self.query

    def delete(self, id):
        """
        This function create delete query.
        :param id: id of the field which needs to be deleted
        :return: delete query
        """
        self.query = "DELETE FROM employee WHERE ID={}".format(id)
        return self.query

    def insert(self):
        """
        This function create insert query for employee table
        :return: insert query
        """
        if self.validation():
            return "INSERT INTO employee (firstName,lastName,email, dob, image, prefix, employment, employer, " \
               "maritalStatus, preferCommun)" \
               "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
               % (self.first_name, self.last_name, self.email, self.dob, self.image, self.prefix, self.employment,
                  self.employer, self.marital_status, self.prefer_commun)
        else:
            raise ValueError('Some fields failed validation.')