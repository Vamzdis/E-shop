from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.product_cart import ProductCart
from app.models.product import Product

from app.models.cart_item import CartItem
from app.database import db
from app.models.product import Product
from flask_login import login_required,current_user

bp = Blueprint("cart", __name__)

@bp.route('/cart')
@login_required
def view_cart():
    user_id = current_user.id
    cart = ProductCart.query.filter_by(user_id=user_id).first()
    if not cart or not cart.cart_items:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('products'))

    return render_template('cart.html', cart=cart)


@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):

    user_id = current_user.id
    product = Product.query.get(product_id)
    if not product or product.quantity <= 0:
        flash('Product is out of stock.', 'danger')
        return redirect(url_for('products'))

    cart = ProductCart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = ProductCart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(products_cart=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(products_cart=cart.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    product.quantity -= 1
    db.session.commit()

    flash('Product added to cart.', 'success')
    return redirect(url_for('products'))

@bp.route('/cart/checkout', methods=['POST'])
@login_required
def checkout():

    user_id = current_user.id
    cart = ProductCart.query.filter_by(user_id=user_id).first()

    if not cart or not cart.cart_items:
        flash('Your cart is empty.', 'info')
        return redirect(url_for('products'))
    
    # purchase handling goes here

    return render_template('cart.html', cart=cart)