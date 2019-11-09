from flask import Flask, render_template, request, redirect, url_for

# from wtforms import StringField, Form, SubmitField
# from wtforms.validators import DataRequired

import sqlite3
db = 'challenge.db'
conn = sqlite3.connect(db)
c = conn.cursor()

application = app = Flask(__name__)

@app.route('/')
def index():
    #load the homepage
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/form')
def form():
    return render_template('form.html')

if __name__ == '__main__':
    app.run()
