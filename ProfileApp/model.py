class Employee:
    def __init__(self, kwargs):
        print()
        print(kwargs)
        print()
        self.first_name = kwargs['firstName']
        self.last_name = kwargs['lastName']
        self.dob = kwargs['dob']
        # self.image = kwargs['image']
        self.prefix = kwargs['prefix']
        self.employment = kwargs['employment']
        self.employer = kwargs['employer']
        self.marital_status = kwargs['maritalStatus']
        self.prefer_commun = kwargs['communication']

    def select(self, *args):
        self.query = "SELECT {} FROM employee".format(','.join(args))
        return self.query

    def delete(self, id):
        self.query = "DELETE FROM employee WHERE ID={}".format(id)
        return self.query

    def insert(self):
        return "INSERT INTO employee (firstName,lastName,dob, prefix, employment, employer, " \
               "maritalStatus, preferCommun)" \
               "VALUES (self.first_name,self.last_name,self.dob,self.prefix,self." \
               "employment,self.employer,self.marital_status,self.prefer_commun)"