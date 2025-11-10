from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_required, current_user
from ..models.models import Book, Cart, CartItem, database

shop = Blueprint("shop", __name__)

@shop.route("/shop")
def index():

    # Obtener el número de página de los parámetros de la URL (por defecto página 1)
    page = request.args.get('page', 1, type=int)
    
    # Número de libros por página
    per_page = 8
    
    # Usar paginate() en lugar de all()
    pagination = Book.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False  # No lanzar error 404 si la página no existe
    )
    
    books = pagination.items
    
    if not books and page > 1:
        flash("No hay libros en esta página.", "warning")
        return redirect(url_for('shop.index'))
    
    return render_template(
        "shop/shop.html", 
        books=books,
        pagination=pagination
    )

# Funciones de control para Carrito

def get_or_create_cart():
    if current_user.is_authenticated:
        # Usuario autenticado
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            database.session.add(cart)
            database.session.commit()
    
    return cart

@shop.route('/add-to-cart/<int:book_id>', methods=['POST'])
@login_required
def add_to_cart(book_id):
    book = Book.query.get_or_404(book_id)
    cart = get_or_create_cart()
    
    # Verificar si el libro ya está en el carrito
    cart_item = CartItem.query.filter_by(cart_id=cart.id, book_id=book_id).first()
    
    if cart_item:
        # Incrementar cantidad
        cart_item.quantity += 1
    else:
        # Crear nuevo item
        cart_item = CartItem(
            cart_id=cart.id,
            book_id=book_id,
            price=book.price,
            quantity=1
        )
        database.session.add(cart_item)
    
    database.session.commit()
    flash(f'"{book.title}" agregado al carrito', 'success')
    return redirect(url_for('shop.index'))

@shop.route('/update-quantity/<int:item_id>', methods=['POST'])
def update_quantity(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    quantity = int(request.form.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        database.session.commit()
        flash('Cantidad actualizada', 'success')
    else:
        database.session.delete(cart_item)
        database.session.commit()
        flash('Item eliminado del carrito', 'info')
    
    return redirect(url_for('shop.cart'))

@shop.route('/remove-from-cart/<int:item_id>', methods=['POST'])
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    database.session.delete(cart_item)
    database.session.commit()
    flash('Item eliminado del carrito', 'info')
    return redirect(url_for('shop.cart'))

@shop.route("/cart")
@login_required
def cart():
    cart = get_or_create_cart()
    return render_template("shop/cart.html", cart = cart)

@shop.route("/checkout")
@login_required
def checkout():
    cart = get_or_create_cart()
    if not cart.items:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('shop.index'))
    
    return render_template(
        'shop/checkout.html', 
        cart = cart
    )