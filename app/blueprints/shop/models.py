from app import db
from datetime import datetime as dt
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField, IntegerField, RadioField
from wtforms.validators import DataRequired

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    price = db.Column(db.Integer)
    image = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), default=1)
    cart = db.relationship("Cart", cascade="all, delete-orphan")
    created_on = db.Column(db.DateTime, default = dt.utcnow)

    def __repr__(self):
        return f'<Product: ID: {self.id} - Name {self.name[:10]}>'

    def set_info(self, data):
        for column in ['name', 'description', 'image', 'price', 'category_id']:
            if column in data:
                setattr(self, column, data[column])

    def new_product(self):
        db.session.add(self)
        db.session.commit()

    def remove_product(self):
        db.session.delete(self)
        db.session.commit()

    def update_product(self):
        db.session.commit()

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    products = db.relationship("Products", cascade="all, delete-orphan", backref='category', lazy=True)

    def __repr__(self):
        return f'<Category: ID: {self.id} - Name:{self.name}>'

    def set_info(self, data):
        for category in ['name']:
            if category in data:
                setattr(self, category, data[category])

    def new_category(self):
        db.session.add(self)
        db.session.commit()

    def remove_category(self):
        db.session.delete(self)
        db.session.commit()

    def update_category(self):
        db.session.commit()

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def __repr__(self):
        return f'<Cart: ID: {self.id}>'

    def set_info(self, data):
        for category in ['product_id']:
            if category in data:
                setattr(self, category, data[category])

    def new_cart(self):
        db.session.add(self)
        db.session.commit()

    def delete_cart(self):
        db.session.delete(self)
        db.session.commit()

    def update_cart(self):
        db.session.commit()

class CreateProductForm(FlaskForm):
    name = StringField('Name')
    description = TextField('Description')
    price = IntegerField('Price')
    image = StringField('Image')
    category = StringField('Category')
    add_product = SubmitField('Add Item')

class CreateCategoryForm(FlaskForm):
    name = StringField('Category')
    add_category = SubmitField('Add Category')

class SearchForm(FlaskForm):
    name = StringField('Search by Name')
    category = RadioField('Search by Category', choices=[(1, 'Test'), (2, 'Clothing'), (3, 'Kitchen'), (4, 'Gaming')])