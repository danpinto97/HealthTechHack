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
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("INSERT INTO user_symptoms VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (self.user_id, self.dosage_left, self.days_since_last_dose, datetime.datetime.now(), Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10))
        conn.commit()

    def user_response(self):
        db = 'hth.db'
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("INSERT INTO user VALUES (?, ?, ?, ?)", (self.user_id, self.dosage_left, self.days_since_last_dose, datetime.datetime.now()))
        conn.commit()

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
    # new_user = User("1", 1, 1)
    # new_user.print_attributes()
    # new_user.user_response()
    User.get_users()
