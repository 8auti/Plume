from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from ..models.models import Book, database

book = Blueprint("book", __name__)

# Vista libro
@book.route("/book/view/<int:id>")
def view(id):
    
    book = Book.query.get(id)
    books = Book.query.limit(9).all()

    if book is None:
        flash("Libro no encontrado.", "danger")
        return redirect(url_for('main.home'))
    
    return render_template("book/view.html", book = book, books = books)

# <----- ABM ----->