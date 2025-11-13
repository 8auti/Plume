from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from app.models.models import Book, database
from .genres import genres

book = Blueprint("book", __name__)

# Vista libro
@book.route("/book/view/<int:id>")
def view(id):
    
    book = Book.query.get(id)

    if book is None:
        flash("Libro no encontrado.", "danger")
        return redirect(url_for('shop.index'))
    

    # Libros relacionados
    related_books = Book.query.filter(
        Book.genre == book.genre,
        Book.id != book.id
    ).limit(6).all()

    # Mas que nada porque no tengo tantos libros creados entonces para que no aparezca un solo libro cargo otros que nada que ver y fue
    related_books =  related_books if len(related_books) > 6 else Book.query.limit(6).all()

    # Obtener otros libros del mismo autor (excluyendo el actual)
    #same_author_books = [b for b in book.author.books if b.id != book.id][:8]
    same_author_books = [b for b in book.author.books][:8]

    return render_template("book/view.html", book = book, related_books = related_books, same_author_books = same_author_books, genres = genres)