from flask import Blueprint, render_template
from ..models.models import Book

main = Blueprint("main", __name__)

@main.route("/")
def home():
    #books = Book.query.limit(9).all()  # Traer hasta 9 libros
    books = Book.query.all()
    return render_template("index.html", books=books)

# Manejar errores
@main.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404