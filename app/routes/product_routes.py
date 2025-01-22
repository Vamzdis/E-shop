from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.product import Product
from flask_login import login_required

bp = Blueprint("product", __name__)


@bp.route('/products')
@login_required
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)