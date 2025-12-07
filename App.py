from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret-key"
DB = "database.db"


def index():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    movies = db.execute("SELECT * FROM Movies").fetchall()
    db.close()
    return render_template("index.html", movies=movies)


app.run(debug=True, port=5000)
