from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
database = SQLAlchemy()

# Modelo de usuario
class User(UserMixin, database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    password_hash = database.Column(database.String(255), nullable=False)
    mail = database.Column(database.String(50), nullable=False, unique=True)
    type = database.Column(database.String(50), nullable=False)
    created_at = database.Column(database.DateTime, default=database.func.now())

class Book(database.Model):
    __tablename__ = 'books'

    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False)
    description = database.Column(database.Text, nullable=True)
    pages = database.Column(database.Integer, nullable=True)
    publish_date = database.Column(database.Date, nullable=True)

    # author_id = database.Column(database.Integer, database.ForeignKey('authors.id'))
