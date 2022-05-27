from flask import Flask, render_template, request, redirect, session
import sqlite3
from sqlite3 import Error
from datetime import datetime

app = Flask(__name__)

DATABASE = "dictionary.db"
app.secret_key = "chacha"

def is_logged_in():
    if session.get('email') is None:
        print('logged out')
        return False
    else:
        print('logged in')
        return True

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
def category(catID):
    con = create_connection(DATABASE)
    query = "SELECT id, maori, english, image FROM definitions WHERE category_id=? ORDER BY maori ASC"
    cur = con.cursor()
    cur.execute(query, (catID, ))
    word_list = cur.fetchall()
    con.close
    return render_template("category.html", logged_in=is_logged_in(), categories=get_categories(), words=word_list)

@app.route('/word/<ID>')
def word(ID):
    con = create_connection(DATABASE)
    query = "SELECT id, maori, english, image, definition, editor_id, editted FROM definitions WHERE id=? ORDER BY maori ASC"
    cur = con.cursor()
    cur.execute(query, (ID, ))
    word_list = cur.fetchall()
    print(word_list)
    query = "SELECT * FROM users WHERE id=?"
    cur = con.cursor()
    cur.execute(query, (word_list[0][5], ))
    editor_list = cur.fetchall()
    print(editor_list)
    con.close()
    return render_template("word.html", logged_in=is_logged_in(), categories=get_categories(), word=word_list[0], editor=editor_list[0])

@app.route('/')
def render_homepage():
    return render_template("home.html", categories=get_categories(), logged_in=is_logged_in())

@app.route('/logout')
def render_logout():
    print(list(session.keys()))
    [session.pop(key) for key in list(session.keys())]
    print(list(session.keys()))
    return redirect('/')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        password = request.form.get('password')

        con = create_connection(DATABASE)
        query = 'SELECT id, fname FROM users WHERE email=? AND password=?'
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

            return redirect("/")

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
        teacher = request.form.get('teacher')

        if password != password2:
            return redirect("/signup?error=Please+make+password+match")
        print(len(password))
        if len(password) < 8:
            return redirect("/signup?error=Please+make+password+at+least+8+characters")

        con = create_connection(DATABASE)

        query = "INSERT INTO users (fname, lname, email, password, teacher) VALUES (?, ?, ?, ?, ?)"
        cur = con.cursor()
        cur.execute(query, (fname, lname, email, password, teacher))
        con.commit()
        con.close()
        return redirect("/login")

    error = request.args.get('error')
    if error == None:
        error = ""

    return render_template("signup.html", error=error)

@app.route('/add_word', methods=['POST', 'GET'])
def add_word():
    if request.method == 'POST':
        print(request.form)
        maori = request.form.get('maori_word').title().strip()
        english = request.form.get('english_word').title().strip()
        cat_id = request.form.get('category')
        date_added = datetime.now()
        definition = request.form.get('definition_word')
        editor_id = session['user_id']
        level = request.form.get('ylevel')
        editted = datetime.now()
        image = 'noimage.png'

        create_connection(DATABASE)

        query = "INSERT INTO defintions(maori, english, cat_id, date_added, definition, editor_id, level, editted, image, id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cur = con.cursor()
        cur.execute(query, (maori, english, cat_id, date_added, definition, editor_id, level, editted, image))
        con.commit()
        con.close()

        return redirect('/')
    return render_template("addword.html", logged_in=is_logged_in(), categories=get_categories())

app.run(host='0.0.0.0', debug=True)
