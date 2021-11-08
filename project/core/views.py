from flask import render_template, Blueprint, request, session
from project.models import Product
from project.core.forms import FilterForm

core = Blueprint("core", __name__)


@core.route("/", methods=["GET", "POST"])
def home():
    page = request.args.get("page", 1, type=int)
    product = Product.query.order_by(Product.id.desc()).paginate(page=page, per_page=8)
    try:
        session["total_quantity"]
    except KeyError:
        session["total_quantity"] = 0
    return render_template("home.html", product=product, page=page, total_quantity=session["total_quantity"])


def product(product_type):
    form = FilterForm()
    products = Product.query.filter_by(category=f"{product_type[:-1]}").all()
    filter_result = request.form.get("subcategory_filter")
    filter_product = []
    for product in products:
        if product.subcategory == filter_result:
            filter_product.append(product)
        elif filter_result == "all products":
            filter_product.append(product)
    return render_template("products.html", form=form, filter_product=filter_product,
                           filter_result=filter_result, products=products, total_quantity=session["total_quantity"])


@core.route("/bracelets", methods=["GET", "POST"])
def bracelets():
    return product("bracelets")


@core.route("/earrings", methods=["GET", "POST"])
def earrings():
    return product("earrings")


@core.route("/necklaces", methods=["GET", "POST"])
def necklaces():
    return product("necklaces")


@core.route("/rings", methods=["GET", "POST"])
def rings():
    return product("rings")


@core.route("/product<int:product_id>", methods=["GET", "POST"])
def about_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template("about_product.html", product=product, total_quantity=session["total_quantity"])
