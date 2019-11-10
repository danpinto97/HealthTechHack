from flask import Flask, render_template, request, redirect, url_for
from model import User
# from wtforms import StringField, Form, SubmitField
# from wtforms.validators import DataRequired

import sqlite3
db = 'challenge.db'
conn = sqlite3.connect(db)
c = conn.cursor()

application = app = Flask(__name__)
elias = User("2", 12, 0)
@app.route('/')
def index():
    elias = User("2", 12, 0)
    #load the homepage
    return render_template('home.html', days_since_inj = elias.last_dose_from_db(), dosage_left = elias.get_remaining_inj_from_db())

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/form', methods=['GET','POST'])
def form():
    if request.method == 'POST':
        try:
            o1 = request.form['inlineRadioOptions']
        except:
            o1 = 0
        try:
            o2 = request.form['inlineRadioOptions2']
        except:
            o2 = 0
        try:
            o3 = request.form['inlineRadioOptions3']
        except:
            o3 = 0

        elias.answer_form(o1,o2,o3,0,0,0,0,0,0,0)
        print(elias.get_indi_sym())
    return render_template('form.html')

if __name__ == '__main__':
    app.run()
