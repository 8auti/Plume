from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("index.html")

# Manejar errores
@main.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('404.html'), 404