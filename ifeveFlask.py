from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)

db_path = 'ifeve/ifeve.db'


@app.route("/")
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
def fetch_by_category(name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ifeve WHERE category = ?", (name,))
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("index.html", values=values)


@app.route("/delete/<id>", methods=["delete"])
def delete_by_id(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ifeve WHERE id = ?", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return 'ok'


@app.route("/article/<id>", methods=["get"])
def read_article(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ifeve WHERE id = ?", (id,))
    value = cursor.fetchall()[0]
    cursor.close()
    conn.close()
    return render_template("article.html", article=value)


if __name__ == "__main__":
    app.run()
