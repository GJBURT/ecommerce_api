# This will be an ecommerce API using Flask and MySQL
# Importing necessary libraries
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from flask_marshmallow import Marshmallow

# Initialize Flask app
app = Flask(__name__)

# MySQL Database connection configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:CodeTemple25@@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating Base Model
Base = declarative_base()

# Initialize SQLAlchemy object and marshmallow
ma = Marshmallow(app)
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Creating the database engine
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# Create all tables in the database to include User, Product, Order, 
# and Order_Product Association tables

# User Table including id, name, address, email that must be unique
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # One to-many relationship one user can have many orders
    orders = db.relationship('Order', backref='user', lazy=True)

# Product Table including id, product_name, and price
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Many to-many relationship one product can be in many orders
    # and one order can have many products
    

# Order Table including id, user_id, and order_date
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)

    # Many to-one relationship one order can have many products
    products = db.relationship('Product', secondary='order_product', lazy='dynamic')

# Order_Product Association Table including order_id and product_id
# Association table must ensure that there are no duplicates of the same product in the same order
class OrderProduct(db.Model):
    __tablename__ = 'order_product'
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)


# Marshmallow schemas for serialization and deserialization
# User Schema
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True
        
# Product Schema
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_relationships = True
        # Include foreign keys in the schema
        include_fk = True
        load_instance = True
        
# Order Schema
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_relationships = True
        # Include foreign keys in the schema
        include_fk = True
        load_instance = True
        
# OrderProduct Schema
class OrderProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderProduct
        include_relationships = True
        # Include foreign keys in the schema
        include_fk = True
        load_instance = True
        

