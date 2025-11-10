from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app.models.models import User
from app import database

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        # Buscar usuario por email
        user = User.query.filter_by(email=email).first()

        # Verificar si existe y la contraseña es correcta
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)  # Flask-Login
            return redirect(url_for('main.home'))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
            return redirect(url_for('auth.login'))
        
    return render_template('auth/login.html')

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]
        user_type = request.form["user_type"]

        # Tipo de usuario vacio (F12)
        if (user_type == '' or user_type == None):
            flash("El tipo de usuario no puede estar vacio.", "danger")
            return redirect(url_for("auth.register"))
        
        # Email vacio
        if (email == '' or email == None):
            flash("El email no puede estar vacio.", "danger")
            return redirect(url_for("auth.register"))
        
        # Contrase;a vacia
        if (password == '' or password == None):
            flash("La contraseña no puede estar vacia.", "danger")
            return redirect(url_for("auth.register"))

        # Contraseñas no coinciden
        if (password != password_confirm):
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for("auth.register"))

        # Buscar usuario por email para evitar error
        already_registered_email = User.query.filter_by(email=email).first()
        if (already_registered_email) :
            flash("El email ingresado ya esta en uso.", "danger")
            return redirect(url_for("auth.register"))
        
        if (user_type != 'editor' and user_type != 'escritor'):
            flash("El tipo de usuario ingresado es invalido.", "danger")
            return redirect(url_for("auth.register"))

        # Crear el hash de la password
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        # Crear usuario y guardar en la base de datos
        nuevo_usuario = User(name=name, password_hash=password_hash, email=email, type=user_type)
        database.session.add(nuevo_usuario)
        database.session.commit()

        flash("Registro exitoso. Ya puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template('auth/register.html')

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("auth.login"))