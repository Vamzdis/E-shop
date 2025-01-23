from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.product import Product
from flask_login import login_required, current_user

bp = Blueprint("product", __name__)


@bp.route('/products')
@login_required
def products():
    products = Product.query.all()
    return render_template('producst_extends_base.html', products=products, user_logged_in=current_user.is_authenticated)