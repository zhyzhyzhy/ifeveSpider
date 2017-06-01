from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import flash
from flask import redirect
from flask import url_for
from functools import wraps
import sqlite3

app = Flask(__name__)

db_path = 'ifeve/ifeve.db'

app.config.update(dict(
    SECRET_KEY='123321123321',
    USERNAME='admin',
    PASSWORD='Zhy331122'
))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect("/index")
    return render_template('login.html', error=error)


@app.route("/index")
@login_required
def hello_world():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ifeve")
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    values.sort(key=lambda var: var[2])
    return render_template("index.html", values=values)


@app.route("/category/<name>")
@login_required
def fetch_by_category(name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ifeve WHERE category = ?", (name,))
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", values=values)


@app.route("/delete/<id>", methods=["delete"])
@login_required
def delete_by_id(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ifeve WHERE id = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return 'ok'


@app.route("/article/<id>", methods=["get"])
@login_required
def read_article(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ifeve WHERE id = ?", (id,))
    value = cursor.fetchall()[0]
    cursor.close()
    conn.close()
    return render_template("article.html", article=value)


@app.route("/article/addToFav/<id>", methods=["put"])
@login_required
def add_to_fav(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE ifeve SET fav = 1 WHERE id = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return 'ok'


@app.route("/article/removeFromFav/<id>", methods=["put"])
@login_required
def remove_from_fav(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE ifeve SET fav = 0 WHERE id = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return 'ok'


@app.route("/fav", methods=["get"])
@login_required
def fav():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ifeve WHERE fav = 1")
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("fav.html", values=values)


if __name__ == "__main__":
    app.run()
