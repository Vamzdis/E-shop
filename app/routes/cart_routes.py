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
    #we're selecting products, their ordered quantities here and the id of this order
    cart_products = db.session.query(Product, CartItem.quantity, ProductCart.id, (Product.price * CartItem.quantity).label('total_price')                        
#the above selection is made from order items where the product item is joined with cart item by id below
).join( CartItem, Product.id == CartItem.product_id 
#that selection is made from cartitems where order id matches       
).join( ProductCart, CartItem.products_cart_id == ProductCart.id 
#lastly, we only select products that are matching the given user id which is listed in the orders table
).filter( ProductCart.user_id == user_id).all()
    

    if not cart_products:
        total_price = 0
        cart_id = None
    else:
        cart_id = cart_products[0][2]
        total_price = sum(product.total_price for product in cart_products)
    return render_template('cart.html', products=cart_products, cart_id=cart_id, total_price=total_price)


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
        cart = ProductCart(user_id=user_id) #it not, then create a new cart
        db.session.add(cart)

        cart_item = CartItem(products_cart_id=cart.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    cart_item = CartItem.query.filter_by(products_cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(products_cart=cart.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()

    flash('Product added to cart.', 'success')
    return redirect(url_for('products'))


@bp.route('/remove_item/<int:id>', methods = ['GET','POST'])
@login_required
def remove_cart_item(id):
    cart_item = CartItem.query.get(id)

    if not cart_item:
        flash('No such item in the cart','danger')
        return redirect(request.url)
    
    if request.method == "POST":
        db.session.delete(cart_item)
        db.session.commit()
        flash(f"Item successfully deleted from the cart",'success')
        return redirect(url_for("cart.view_cart"))             
    else:
        return render_template("cart.html", cart_item = cart_item) 