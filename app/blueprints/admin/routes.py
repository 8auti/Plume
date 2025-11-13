import os
import boto3
import mimetypes

from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.models.models import Book, database
from ..book.genres import genres
from dotenv import load_dotenv

# Acceder a variables de entorno
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("ACCESS_KEY_S3")
AWS_SECRET_ACCESS_KEY = os.getenv("SECRET_KEY_ACCESS_S3")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME", "da-vinci-ejemplo1")

admin = Blueprint("admin", __name__)

# Dashboard

@admin.route("/admin")
@login_required
def dashboard():
    # El escritor ve solo sus libros
    if current_user.type == 'escritor':
        books = Book.query.filter_by(author_id=current_user.id).all()
    # El editor ve todos los libros
    elif current_user.type == 'editor':
        books = Book.query.all()

    # TODO: Agregar paginacion
    return render_template("admin/dashboard.html", books = books)


# Funcion para subir archivos a AWS

def upload_image(file):
    filename = secure_filename(file.filename)
    if not filename:
        flash("El archivo subido no tiene un nombre válido.", "danger")
        return

    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    try:
        # Crear cliente de S3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        # Subir archivo a S3
        s3.upload_fileobj(
            file,
            AWS_S3_BUCKET_NAME,
            filename,
            ExtraArgs={"ContentType": content_type}
        )

        # URL pública
        file_url = f"https://{AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{filename}"

        return file_url

    except Exception as e:
        flash("Error al subir la imagen.", "danger")

# Crear libro

@admin.route("/admin/create/", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        pages = request.form["pages"]
        description = request.form["description"]
        genre = request.form.get('genre')
        price = request.form["price"]
        cover = request.files["cover"]

        if (not title or not pages or not price):
            flash("Completa todos los campos", "danger")
            return redirect(url_for('admin.create'))
        
        # Validar que el genero sea autentico
        if (genre not in genres and genre != ''): # Permitir que el genero sea un string vacio (Ninguno)
            flash("Genero invalido.", "danger")
            return render_template('admin/form.html', genres = genres)

        # Portada
        cover_url = upload_image(cover)

        # fk usuario escritor
        author_id = current_user.id

        new_book = Book(
            title=title, 
            pages=pages, 
            description=description, 
            genre = genre, 
            author_id=author_id, 
            cover_url = cover_url
        )

        database.session.add(new_book)
        database.session.commit()
        flash("Libro agregado exitosamente", "success")

        return redirect(url_for('admin.dashboard'))
    return render_template("admin/form.html", genres=genres)


# Editar libro


@admin.route("/admin/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    book = Book.query.get_or_404(id)
    
    if request.method == "POST":
        if current_user.type == 'escritor':

            book.title = request.form['title']
            book.pages = request.form.get('pages')
            book.description = request.form.get('description')
            book.price = request.form.get('price')
            genre = request.form.get('genre')
            cover = request.files["cover"]

            # Validar que el genero sea autentico
            if (genre not in genres and genre != ''): # Permitir que el genero sea un string vacio (Ninguno)
                flash("Genero invalido.", "danger")
                return render_template('admin/form.html', book=book, genres = genres)

            book.genre = genre

            if (cover or cover.filename != ''):
                book.cover_url = upload_image(cover) or book.cover_url

        elif current_user.type == 'editor':

            book.status = request.form['status'] or 'pendiente'
            book.published_books = request.form.get('books_to_publish') or 0
            book.profit_percentage = request.form.get('profit_percentage') or 0

        # Guardar datos
        database.session.commit()
        flash(f"Libro actualizado con exito.", "success")

        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/form.html', book=book, genres = genres)



# Eliminar libro

@admin.route("/admin/delete/<int:id>", methods=["POST", "GET"])
@login_required
def delete(id):
    book = Book.query.get(id)
    if book is None:
        flash("Libro no encontrado", "error")
        return redirect(url_for('admin.dashboard'))
    
    database.session.delete(book)
    database.session.commit()

    flash(f"Libro '{book.title}' eliminado exitosamente", "danger")
    return redirect(url_for('admin.dashboard'))  # Redirige a la lista de libros