from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from app.models.user import User
# from flask import request, redirect, url_for #very likely will need these in the nearby future

from app.database import db

from app.models.product import Product
from app.models.dummies import dummy_products

bp = Blueprint('shop', __name__)

@bp.route('/')
def show():
    products = Product.query.filter_by(is_deleted=False).all()
    return render_template("products_extends_base.html", products=products)


@bp.route("/product/<int:id>")
def view_product(id):
    product = Product.query.get(id)
    if current_user.is_admin:
        return render_template("view_product_admin.html", product = product)
    else:
        return render_template("user/view_product.html", product = product)
