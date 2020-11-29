from app import db
from . import bp as shop
from flask import render_template, redirect, url_for, request
from .models import Products, Categories, CreateProductForm, CreateCategoryForm, Cart
from datetime import datetime as dt

@shop.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'products' : Products.query.filter(Products.category_id != 1).all(),
        'cart' : Cart.query.all()
    }
    return render_template('shop/index.html', **context)

@shop.route('/new_product', methods=['GET', 'POST'])
def new_product():
    create_product = CreateProductForm()
    if create_product.validate_on_submit():
        new_product = Products()
        product_data = {
            'name' : create_product.name.data,
            'description' : create_product.description.data,
            'image' : create_product.image.data,
            'price' : create_product.price.data,
            'category_id' : Categories.query.filter(Categories.name == create_product.category.data).first().id
        }
        new_product.set_info(product_data)
        new_product.new_product()
        return redirect(url_for('shop.new_product'))
    context = {
        'create_product' : create_product,
        'cart' : Cart.query.all()
    }
    return render_template('shop/new_product.html', **context)

@shop.route('/new_category', methods=['GET', 'POST'])
def new_category():
    create_category = CreateCategoryForm()
    if create_category.validate_on_submit():
        new_category = Categories()
        category_data = {
            'name' : create_category.name.data,
        }
        new_category.set_info(category_data)
        new_category.new_category()
        return redirect(url_for('shop.new_category'))
    context = {
        'create_category' : create_category,
        'cart' : Cart.query.all()
    }
    return render_template('shop/new_category.html', **context)

@shop.route('/item', methods=['GET','POST'])
def item():
    item = request.args.get('id')
    context = {
        'product':Products.query.get(item),
        'cart' : Cart.query.all()
    }
    return render_template('shop/item.html', **context)

@shop.route('/add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
    new_cart = Cart()
    product_id = request.args.get('id')
    cart_data = {
        'product_id' : product_id,
    }
    new_cart.set_info(cart_data)
    new_cart.new_cart()
    return redirect(url_for('shop.index'))

@shop.route('/cart', methods=['GET', 'POST'])
def cart():
    my_cart = Cart()
    context = {
        'contents': [Products.query.get(item.product_id) for item in Cart.query.all()],
        'cart' : Cart.query.all()
    }
    return render_template('shop/cart.html', **context)

@shop.route('/remove_from_cart', methods=['GET', 'POST'])
def remove_from_cart():
    product_id = request.args.get('id')
    [db.session.delete(Cart.query.filter_by(product_id=product_id).first())]
    db.session.commit()
    return redirect(url_for('shop.cart'))

