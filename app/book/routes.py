from flask import Blueprint, render_template, request, flash, url_for, redirect
from ..models.models import Book, database

book = Blueprint("book", __name__)

# Listado de libros
@book.route("/book/")
def index():
    books = Book.query.all()
    return render_template("book/index.html", books = books)

# Vista libro
@book.route("/book/view/<int:id>")
def view(id):
    book = Book.query.get(id)

    if book is None:
        flash("Libro no encontrado", "error")
        return redirect(url_for('book.index'))
    
    return render_template("book/view.html", book = book)

# <----- ABM ----->

# Crear libro
@book.route("/book/create/", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        pages = request.form["pages"]
        description = request.form["description"]

        # portada
        # fk usuario escritor

        new_book = Book(title=title, pages=pages, description=description)

        database.session.add(new_book)
        database.session.commit()
        flash("Libro agregado exitosamente", "success")

        return redirect(url_for('book.index'))
    return render_template("book/form.html")

# Editar libro
@book.route("/book/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    book = Book.query.get_or_404(id)
    
    if request.method == "POST":
        book.title = request.form['title']
        book.pages = request.form.get('pages')
        book.description = request.form.get('description')

        database.session.commit()
        flash("Libro actualizado exitosamente", "success")

        return redirect(url_for('book.index'))
    
    return render_template('book/form.html', book=book)  # pasa el libro

# Eliminar libro
@book.route("/book/delete/<int:id>", methods=["POST", "GET"])
def delete(id):
    book = Book.query.get(id)
    if book is None:
        flash("Libro no encontrado", "error")
        return redirect(url_for('book.index'))
    
    database.session.delete(book)
    database.session.commit()

    flash(f"Libro '{book.title}' eliminado exitosamente", "warning")
    return redirect(url_for('book.index'))  # Redirige a la lista de libros