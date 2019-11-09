import sqlite3
import datetime

db = 'hth.db'
conn = sqlite3.connect(db)
c = conn.cursor()

# c.execute("""CREATE TABLE user(
#                     user_id text,
#                     dosage_left integer,
#                     days_since_last_dose integer,
#                     time timestamp,
#                     PRIMARY KEY(user_id)
#                     )""")
# conn.commit()
#
# c.execute("""CREATE TABLE user_symptoms(
#                     user_id text,
#                     dosage_left integer,
#                     days_since_last_dose integer,
#                     time timestamp,
#                     Q1 integer,
#                     Q2 integer,
#                     Q3 integer,
#                     Q4 integer,
#                     Q5 integer,
#                     Q6 integer,
#                     Q7 integer,
#                     Q8 integer,
#                     Q9 integer,
#                     Q10 integer,
#                     PRIMARY KEY(user_id)
#                     )""")
# conn.commit()
