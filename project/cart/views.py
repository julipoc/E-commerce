from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from project.models import Product, Order, Cart
from project.admin.forms import AddOrderForm
from project import db

carts = Blueprint("carts", __name__)


def cart_function():
    products = []
    total_price = 0
    index = 0
    session["total_quantity"] = 0

    if "cart" in session:
        for item in session["cart"]:
            product = Product.query.filter_by(id=item["id"]).first()

            quantity = int(item["quantity"])
            total = quantity * product.price
            total_price += total
            session["total_quantity"] += quantity

            products.append({"id": product.id, "name": product.name, "price": product.price, "image": product.image,
                             "quantity": quantity, "total": total, "index": index})
            index += 1

    total_plus_shipping = total_price + 10
    return products, total_price, total_plus_shipping, session["total_quantity"]


@carts.route("/cart", methods=["POST", "GET"])
def cart():
    products, total_price, total_plus_shipping, total_quantity = cart_function()
    return render_template("cart.html", products=products, total_price=total_price,
                           total_plus_shipping=total_plus_shipping, total_quantity=total_quantity)


@carts.route("/add_to_cart", methods=["POST", "GET"])
def add_to_cart():
    if "cart" not in session:
        session["cart"] = []

    session["cart"].append({"id": request.form.get("product_id"), "quantity": request.form.get("quantity")})
    session.modified = True
    return redirect(url_for("carts.cart"))


@carts.route("/remove_from_cart/<index>")
def remove_from_cart(index):
    del session["cart"][int(index)]
    session.modified = True
    return redirect(url_for("carts.cart"))


@carts.route("/checkout", methods=["POST", "GET"])
def checkout():
    form = AddOrderForm()
    products, total_price, total_plus_shipping, total_quantity = cart_function()
    if form.validate_on_submit():
        order = Order(first_name=form.first_name.data,
                      last_name=form.last_name.data,
                      email=form.email.data,
                      country=form.country.data,
                      city=form.city.data,
                      zip_code=form.zip_code.data,
                      address=form.address.data,
                      card_number=form.card_number.data,
                      security_number=form.security_number.data,
                      card_date=form.card_date.data)

        for product in products:
            order_item = Cart(quantity=product["quantity"], product_id=product["id"])
            order.items.append(order_item)

            product = Product.query.filter_by(id=product["id"]).update({"stock": Product.stock - product["quantity"]})

        db.session.add(order)
        db.session.commit()

        session["cart"] = []
        session.modified = True
        flash("Thank you for your order!")
        return redirect(url_for("carts.cart"))
    return render_template("checkout.html", form=form, total_price=total_price,
                           total_plus_shipping=total_plus_shipping, total_quantity=total_quantity)
