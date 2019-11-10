import sqlite3
import datetime

class User(object):
    '''User class which is our model'''
    def __init__(self, user_id, dosage_left, days_since_last_dose):
        self.user_id = user_id
        self.dosage_left = dosage_left
        self.days_since_last_dose = days_since_last_dose

    def set_user_id(self, _id):
        self.user_id = _id

    def get_user_id(self):
        return self.user_id

    def set_dosage_left(self, dosage):
        self.dosage_left = dosage

    def get_dosage_left(self):
        return self.dosage_left

    def set_days_since_last_dose(self, num_days):
        self.days_since_last_dose = num_days

    def get_days_since_last_dose(self):
        return self.days_since_last_dose

    def decrement_dosage_left(self):
        self.dosage_left = self.dosage_left - 1

    def decrement_days_since_last_dose(self):
        self.days_since_last_dose = self.days_since_last_dose - 1

    def print_attributes(self):
        return ("User ID: %s \nDosage Left: %s \nDays Since Last Dosage: %s \n" % (
        self.user_id, self.dosage_left, self.days_since_last_dose))

    def answer_form(self, Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10):
        """
        Stores a users answers to the form questions in addition to their days since last dosage
        and dosage left and timestamp.
        """
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("INSERT INTO user_symptoms VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.user_id, self.dosage_left, self.days_since_last_dose, datetime.datetime.now(), Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10))
        conn.commit()

    def user_response(self):
        """
        Stores a user and their injection and dosage left in the user database
        """
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (self.user_id, self.dosage_left, self.days_since_last_dose, datetime.datetime.now()))
        conn.commit()

    def reup(self,dosage):
        """
        Stores a user and their injection and dosage left IF they have updated their amount of dosage left
        """
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (self.user_id, dosage, self.days_since_last_dose, datetime.datetime.now()))
        conn.commit()

    def just_dosed(self):
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (self.user_id, self.dosage_left-1, 0, datetime.datetime.now()))
        conn.commit()

    def last_medication_date(self):
        """
        Returns latest day in which a patient was medicated.
        """
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE user_id is ? ORDER BY time DESC LIMIT 1", self.user_id)
        data = c.fetchall()
        print(data)

    def last_dose_from_db(self):
        '''
        Returns difference in days since last injection. We should store this in a db after completed.
        '''
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE user_id is ? ORDER BY time DESC LIMIT 1", self.user_id)
        data = c.fetchall()
        previous_date = data[0][3]
        previous_date = datetime.datetime.strptime(previous_date, '%Y-%m-%d %H:%M:%S.%f')
        d = datetime.datetime.today() - previous_date
        return d.days

    def get_remaining_inj_from_db(self):
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE user_id is ? ORDER BY time DESC LIMIT 1", self.user_id)
        data = c.fetchall()
        return data[0][1]

    def get_indi_sym(self):
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT * FROM user_symptoms WHERE user_id is ?", self.user_id)
        data = c.fetchall()
        return data

    @classmethod
    def get_recent_user_from_id(self, id):
        """
        Returns latest day in which a patient was medicated.
        """
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE user_id is ? ORDER BY time DESC LIMIT 1", id)
        data = c.fetchall()
        return User(id, data[0][1], data[0][2])

    @classmethod
    def get_sym(self):
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT * FROM user_symptoms")
        data = c.fetchall()
        print(data)

    @classmethod
    def get_users(self):
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT * FROM user")
        data = c.fetchall()
        print(data)

if __name__ == '__main__':
    #new_user = User("2", 1, 0)
    # new_user.print_attributes()
    # new_user.user_response()
    User.get_users()
    #new_user.last_dose_from_db()
