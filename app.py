from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error
from datetime import datetime
app = Flask(__name__)

DATABASE = "dictionary.db"


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return none

def get_categories():
    con = create_connection(DATABASE)
    query = "SELECT id, name FROM category"
    cur = con.cursor()
    cur.execute(query)
    categories = cur.fetchall()
    con.close()
    return categories

@app.route('/category/<catID>')
def categories(catID):
    return render_template("category.html", categories=get_categories())


@app.route('/')
def render_homepage():
    return render_template("home.html", categories=get_categories())



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        password = request.form.get('password')

        con = create_connection(DATABASE)
        query = 'SELECT id, fname FROM student_users WHERE email=? AND password=?'
        cur = con.cursor()
        cur.execute(query, (email, password))
        user_data = cur.fetchall()
        con.close()

        if user_data:
            users = user_data[0][0]
            first_name = user_data[0][1]
            print(users, first_name)

            session['email'] = email
            session['users'] = users
            session['fname'] = first_name

            return redirect("/menu")

        else:
            return redirect("/login?error=Incorrect+username+or+password")

    return render_template("login.html")


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        print(request.form)
        fname = request.form.get('fname').title().strip()
        lname = request.form.get('lname').title().strip()
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('confirm_password')

        if password != password2:
            return redirect("/signup?error=Please+make+password+match")
        print(len(password))
        if len(password) < 8:
            return redirect("/signup?error=Please+make+password+at+least+8+characters")

        con = create_connection(DATABASE)

        query = "INSERT INTO student_users (fname, lname, email, password) VALUES (?, ?, ?, ?)"
        cur = con.cursor()
        cur.execute(query, (fname, lname, email, password))
        con.commit()
        con.close()
        return redirect("/login")

    error = request.args.get('error')
    if error == None:
        error = ""

    return render_template("signup.html", error=error)





app.run(host='0.0.0.0', debug=True)
