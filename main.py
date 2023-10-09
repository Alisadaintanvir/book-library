from flask import Flask, render_template, request, redirect, url_for
from flask_migrate import Migrate
from db import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"

db.init_app(app)

migrate = Migrate(app, db)


@app.route('/')
def home():
    return render_template("index.html", books=Book.query.all())


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(title=request.form['bookName'],
                        author=request.form['author'],
                        rating=request.form['rating']
                        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form['id']
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('home'))

    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template('edit.html', book=book_selected)


if __name__ == "__main__":
    app.run(debug=True)
