from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
database = SQLAlchemy()

# Modelo de usuario
class User(UserMixin, database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    password_hash = database.Column(database.String(255), nullable=False)
    email = database.Column(database.String(50), nullable=False, unique=True)
    type = database.Column(database.String(50), nullable=False) # writer, editor
    created_at = database.Column(database.DateTime, default=database.func.now())

class Book(database.Model):
    __tablename__ = 'books'

    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(100), nullable=False, default='Libro')
    description = database.Column(database.Text, nullable=True)
    genre = database.Column(database.String(20), nullable=False)
    pages = database.Column(database.Integer, nullable=True)
    price = database.Column(database.Float, default=15000.0)
    status = database.Column(database.String(50), default='draft')  # draft, in_review, approved, published
    cover_url = database.Column(database.String(200), nullable=True)

    author_id = database.Column(database.Integer, database.ForeignKey('users.id'))
    
    # Relación para acceder fácilmente al autor
    author = database.relationship('User', backref='books')

    publish_date = database.Column(database.DateTime, default=database.func.now())
    last_update = database.Column(database.DateTime, default=database.func.now(), onupdate=database.func.now())


class Cart(database.Model):
    __tablename__ = 'carts'
    
    id = database.Column(database.Integer, primary_key=True)
    user_id = database.Column(database.Integer, database.ForeignKey('users.id'), nullable=True)  # Nullable para carritos de invitados
    session_id = database.Column(database.String(100), nullable=True)  # Para usuarios no autenticados
    created_at = database.Column(database.DateTime, default=database.func.now())
    updated_at = database.Column(database.DateTime, default=database.func.now(), onupdate=database.func.now())
    
    # Relaciones
    items = database.relationship('CartItem', backref='cart', lazy=True, cascade='all, delete-orphan')
    user = database.relationship('User', backref='carts')
    
    def __repr__(self):
        return f'<Cart {self.id}>'
    
    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.items)
    
    @property
    def total(self):
        return self.subtotal * 1.21  # Con IVA del 21%
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items)
    
class CartItem(database.Model):
    __tablename__ = 'cart_items'
    
    id = database.Column(database.Integer, primary_key=True)
    cart_id = database.Column(database.Integer, database.ForeignKey('carts.id'), nullable=False)
    book_id = database.Column(database.Integer, database.ForeignKey('books.id'), nullable=False)
    quantity = database.Column(database.Integer, default=1, nullable=False)
    price = database.Column(database.Float, nullable=False)  # Guardar precio en el momento de agregar
    created_at = database.Column(database.DateTime, default=database.func.now())
    
    # Relaciones
    book = database.relationship('Book', backref='cart_items')
    
    def __repr__(self):
        return f'<CartItem {self.id} - Book: {self.book_id} x{self.quantity}>'
    
    @property
    def subtotal(self):
        return self.price * self.quantity