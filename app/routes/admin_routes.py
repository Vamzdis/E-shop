
from app import app
from flask import render_template, request, redirect, url_for
from app.models.product import Product
from database import db
from sqlalchemy import func
from app.models.user import User


@app.route("/add_product", methods = ["GET", "POST"])
def add_product():
    if request.method == "POST":
        try:
            name = request.form["name"]
            description = request.form["description"]
            price = float(request.form["price"])
            quantity = int(request.form["quantity"])
        except ValueError as e: 
            error_message = str(e)
            return render_template("...", error_message = error_message)        #add template
        
        is_available = quantity > 0
        is_deleted = False
        created_on = func.now()
        picture = "???"                             #add picture????

        product = Product(
            name=name, description=description, 
            price=price, 
            quantity=quantity, 
            is_available=is_available, 
            is_deleted=is_deleted,
            created_on = created_on
            )
        
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("..."))         #add template
    else:
        return render_template("...")           #add template


@app.route("/list_products")
def list_products():
    products = Product.query.all()
    return render_template("...", products=products)    #add template


@app.route("/delete_producct/<int:id>", methods = ["GET", "POST"])
def delete_product(id):
    product = Product.query.get(id)

    if not product:
        return "Product not found", 404

    if request.method == "POST":
        product.is_deleted = True
        db.session.commit()
        return redirect(url_for("..."))         #add template
    else:
        return render_template("...", product=product)      #add template


@app.route("/edit_product/<int:id>", methods = ["GET", "POST"])
def edit_product(id):
    product = Product.query.get(id)

    if not product:
        return "Product not found", 404

    if request.method == "POST":
        try:
            name = request.form.get("name")
            description = request.form.get("description")
            price = request.form.get("price")
            quantity = request.form.get("quantity")

            if name:
                product.name = name
            if description:
                product.description = description
            if price:
                product.price = float(price)
            if quantity:
                product.quantity = int(quantity)

            if "BUTTON_NAME_HERE" in request.form:      # insert restore button name here
                product.is_deleted = False
            else:
                product.is_deleted = product.is_deleted
            
            product.is_available = product.quantity > 0

        except ValueError as e: 
            error_message = str(e)
            return render_template("...", error_message = error_message)    #add url
        return redirect(url_for("..."))
    return render_template("...", product = product)            #add url


@app.route("/list_users")
def list_users():
    users = Product.query.all()
    return render_template("...", users=users)      #add template


@app.route("/delete_user/<int:id>", methods = ["GET", "POST"])
def delete_user(id):
    user = User.query.get(id)

    if not user:
        return "User not found", 404
    
    if request.method == "POST":
        user.is_deleted = True
        db.session.commit()
        return redirect(url_for("..."))             #add template
    else:
        return render_template("...", user = user)  #add template
    

# Administratoriaus galimybės


# Papildyti esamų prekių kiekį

# Peržiūrėti statistika apie prekes. Kiek prekių nupirkta kurią dieną, už kiek nupirkta,
# kurie mėnesiai pelningiausi, kurios prekės geriausiai įvertintos

