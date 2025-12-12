from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret-key"
DB = "DATABASE/Movie_App.db"


@app.route("/")
def index():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    movies = db.execute("SELECT * FROM Movies").fetchall()
    db.close()
    return render_template("index.html", movies=movies)


@app.route("/movie/<int:id>")
def movie_page(id):
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    movie = db.execute("SELECT * FROM Movies WHERE id = ?", (id,)).fetchone()
    reviews = db.execute(
        """
        SELECT Reviews.*, Users.username 
        FROM Reviews 
        JOIN Users ON Reviews.UserID = Users.id
        WHERE MovieID = ?
    """,
        (id,),
    ).fetchall()

    db.close()
    return render_template("movie.html", movie=movie, reviews=reviews)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        db = sqlite3.connect(DB)
        db.execute(
            "INSERT INTO Users (username, password) VALUES (?, ?)", (username, password)
        )
        db.commit()
        db.close()
        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = sqlite3.connect(DB)
        db.row_factory = sqlite3.Row
        user = db.execute(
            "SELECT * FROM Users WHERE username = ?", (username,)
        ).fetchone()
        db.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect("/")
        else:
            return "Incorrect username or password"
    return render_template("login.html")


@app.route("/logout")
def Logout():
    session.clear()
    return redirect("/")


@app.route("/movie/<int:id>/add_review", methods=["POST"])
def add_review(id):
    if "user_id" not in session:
        return "Please log in before leaving a review"
    rating = request.form["Rating"]
    review = request.form["Review"]
    db = sqlite3.connect(DB)
    db.execute(
        """
        INSERT INTO Reviews (Date, Review, Rating, MovieID, UserID)
        VALUES (CURRENT_DATE, ?, ?, ?, ?)
    """,
        (review, rating, id, session["user_id"]),
    )

    db.commit()
    db.close()
    return redirect(f"/movie/{id}")


@app.route("/review/<int:id>/delete")
def delete_review(id):
    if "user_id" not in session:
        return "Please log in before deleting your review"
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    review = db.execute("SELECT * FROM Reviews WHERE id = ?", (id,)).fetchone()

    if review["UserID"] != session["user_id"]:
        db.close()
        return "Not allowed"
    db.execute("DELETE FROM Reviews WHERE id = ?", (id,))
    db.commit()
    db.close()
    return redirect("/")


@app.route("/review/<int:id>/edit", methods=["GET", "POST"])
def edit_review(id):
    if "user_id" not in session:
        return "Please log in before editing your review"
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    review = db.execute("SELECT * FROM Reviews WHERE id = ?", (id,)).fetchone()

    if review["UserID"] != session["user_id"]:
        db.close()
        return "Invalid request"
    if request.method == "POST":
        new_text = request.form["Review"]
        new_rating = request.form["Rating"]

        db.execute(
            "UPDATE Reviews SET Review = ?, Rating = ? WHERE id = ?",
            (new_text, new_rating, id),
        )
        db.commit()
        db.close()
        return redirect(f"/movie/{review['MovieID']}")
    db.close()
    return render_template("edit_review.html")


app.run(debug=True, port=5000)
