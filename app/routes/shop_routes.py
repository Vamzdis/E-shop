from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

from app.database import db

from app.models.product import Product
from app.models.user import User

bp = Blueprint('shop', __name__)

@bp.route('/')
def show():

    if current_user.is_authenticated and current_user.is_admin:
        products = Product.query.filter_by(is_deleted=False).all()  

    else:
        #using filter here because you cant use quantity comparisons in filter by
        products = Product.query.filter(Product.is_deleted == False, Product.quantity > 0 ).all()


    return render_template("products_extends_base.html", products=products)

@bp.route("/product/<int:id>")
def view_product(id):
    product = Product.query.get(id)
    if current_user.is_admin:
        return render_template("view_product_admin.html", product = product)
    else:
        return render_template("user/view_product.html", product = product)
