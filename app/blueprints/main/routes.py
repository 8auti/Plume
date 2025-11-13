from flask import Blueprint, render_template
from app.models.models import Book

main = Blueprint("main", __name__)

@main.route("/")
def home():
    #books = Book.query.limit(9).all()  # Traer hasta 9 libros
    books = Book.query.limit(5).all()
    return render_template("index.html", books=books)