from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from ..models.models import Book, database

book = Blueprint("book", __name__)

# Vista libro
@book.route("/book/view/<int:id>")
def view(id):
    
    book = Book.query.get(id)

    # Libros relacionados (chamuyo)
    related_books = Book.query.limit(9).all()

    # Obtener otros libros del mismo autor (excluyendo el actual)
    #same_author_books = [b for b in book.author.books if b.id != book.id][:8]
    same_author_books = [b for b in book.author.books][:8]


    if book is None:
        flash("Libro no encontrado.", "danger")
        return redirect(url_for('main.home'))
    
    return render_template("book/view.html", book = book, related_books = related_books, same_author_books = same_author_books)

# <----- ABM ----->