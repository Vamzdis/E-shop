from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.product_cart import ProductCart
from app.models.product import Product

from app.models.cart_item import CartItem
from app.models.user import User

from app.database import db
from app.models.product import Product
from flask_login import login_required,current_user

bp = Blueprint("cart", __name__)

@bp.route('/cart')
@login_required
def view_cart():
    user_id = current_user.id

    #oh boy this needs explaination
    cart_products = db.session.query(Product, CartItem.quantity, ProductCart.id, (Product.price * CartItem.quantity).label('total_price')                        
).join( CartItem, Product.id == CartItem.product_id       
).join( ProductCart, CartItem.products_cart_id == ProductCart.id 
).filter( ProductCart.user_id == user_id).all()
    

    if not cart_products:
        total_price = 0
        cart_id = None
    else:
        cart_id = cart_products[0][2]
        total_price = sum(product.total_price for product in cart_products)
    return render_template('cart_extends_base.html', products=cart_products, cart_id=cart_id, total_price=total_price)


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
        return redirect(request.referrer)

    cart = ProductCart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = ProductCart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(products_cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        if cart_item.quantity + 1 > product.quantity:
            flash(f"Only {product.quantity} units available in stock.", "danger")
            return redirect(request.referrer)

        cart_item.quantity += 1
    else:

        if product.quantity < 1:
            flash("No units available in stock.", "danger")
            return redirect(request.referrer)

        cart_item = CartItem(products_cart_id=cart.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    flash('Product added to cart.', 'success')
    return redirect(request.referrer)

@bp.route('/remove_item/<int:id>', methods=['POST'])
@login_required
def remove_cart_item(id):
   
    user_cart = ProductCart.query.filter_by(user_id=current_user.id).first()

    if not user_cart:
        flash('No cart found for the current user.', 'danger')
        return redirect(url_for('cart.view_cart'))

    cart_item = CartItem.query.filter_by(product_id=id, products_cart_id=user_cart.id).first()

    if not cart_item:
        flash('No such item in your cart.', 'danger')
        return redirect(request.referrer)

    db.session.delete(cart_item)
    db.session.commit()

    flash('Item successfully deleted from the cart.', 'success')
    return redirect(url_for('cart.view_cart'))
