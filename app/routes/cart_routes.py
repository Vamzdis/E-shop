from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.product_cart import ProductCart
from app.models.product import Product

from app.models.cart_item import CartItem
from app.models.order_item import OrderItem
from app.models.order import Order

from app.database import db
from app.models.product import Product
from flask_login import login_required,current_user

bp = Blueprint("cart", __name__)

@bp.route('/cart')
@login_required
def view_cart():
    user_id = current_user.id

    #oh boy this needs explaination
    #we're selecting products, their ordered quantities here and the id of this order
    cart_products = db.session.query(Product, OrderItem.quantity, Order.id, Order.purchase_price                                 
#the above selection is made from order items where the product item is joined with oder item by id below
).join( OrderItem, Product.id == OrderItem.product_id 
#that selection is made from oders where order id matches       
).join( Order, OrderItem.order_id == Order.id 
#lastly, we only select products that are matching the given user id which is listed in the orders table
).filter( Order.user_id == user_id).all()
    
    order_id = cart_products[0][2]
    price = cart_products[0][3]

    return render_template('cart.html', products=cart_products, order_id=order_id, price=price)


@bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):

    if not current_user.is_authenticated:
        flash("You need to log in to add items to your cart.", "warning")
        return redirect(url_for('auth.login', next=url_for('cart.add_to_cart', product_id=product_id)))

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


#pretty sure this is redundant now
# @bp.route('/cart/checkout', methods=['POST'])
# @login_required
# def checkout():

#     user_id = current_user.id
#     cart = ProductCart.query.filter_by(user_id=user_id).first()

#     if not cart or not cart.cart_items:
#         flash('Your cart is empty.', 'info')
#         return redirect(url_for('products'))
    
#     # purchase handling goes here

#     return render_template('cart.html', cart=cart)