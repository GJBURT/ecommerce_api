# This will be an ecommerce API using Flask and MySQL
# Importing necessary libraries
import os
from flask import Flask, jsonify, request
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
        
# CRUD Endpoints for User, Product, Order, and Order_Product Association tables
# User Endpoints 
# Get/users:Retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return user_schema.jsonify(users)

# Get/users/<id>:Retrieve a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    user_schema = UserSchema()
    return user_schema.jsonify(user)

# POST/users:Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    user_schema = UserSchema()
    new_user = user_schema.load(request.json, session=db.session)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

# PUT/users/<id>:Update a user by id
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    user_schema = UserSchema()
    updated_user = user_schema.load(request.json, instance=user, session=db.session)
    db.session.commit()
    return user_schema.jsonify(updated_user)

# DELETE/users/<id>:Delete a user by id
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"{user.name} was successfully deleted."}), 204

# Product Endpoints
# Get/products:Retrieve all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_schema = ProductSchema(many=True)
    return product_schema.jsonify(products)

# Get/products/<id>:Retrieve a product by id
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    product_schema = ProductSchema()
    return product_schema.jsonify(product)

# POST/products:Create a new product
@app.route('/products', methods=['POST'])
def create_product():
    product_schema = ProductSchema()
    new_product = product_schema.load(request.json, session=db.session)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product), 201

# PUT/products/<id>:Update a product by id
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    product_schema = ProductSchema()
    updated_product = product_schema.load(request.json, instance=product, session=db.session)
    db.session.commit()
    return product_schema.jsonify(updated_product)

# DELETE/products/<id>:Delete a product by id
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"{product.name} was successfully Deleted."}), 204

# Order Endpoints
# Get/orders:Retrieve all orders for a user
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    order_schema = OrderSchema(many=True)
    return order_schema.jsonify(orders)

# Get/orders/<id>:Retrieve an order by id
@app.route('/orders/<int:id>', methods=['GET']) 
def get_order(id):
    order = Order.query.get_or_404(id)
    order_schema = OrderSchema()
    return order_schema.jsonify(order)

# POST/orders:Create a new order
@app.route('/orders', methods=['POST'])
def create_order():
    order_schema = OrderSchema()
    new_order = order_schema.load(request.json, session=db.session)
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order), 201

# PUT/orders/<order_id>/add_product/<product_id>:Add a product to an order (prevent duplicates)
@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(product_id)
    
    # Check if the product is already in the order
    if product in order.products:
        return {'message': 'Product already in order'}, 400
    
    order.products.append(product)
    db.session.commit()
    return jsonify({"message": f"{product.name} was successfully added to the order: {order.id}"}), 204

# DELETE/orders/<order_id>/remove_product/<product_id>:Remove a product from an order
@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
def remove_product_from_order(order_id, product_id):
    order = Order.query.get_or_404(order_id)
    product = Product.query.get_or_404(product_id)
    
    # Check if the product is in the order
    if product not in order.products:
        return {'message': f'{Product.name} not in order'}, 400
    
    order.products.remove(product)
    db.session.commit()
    return jsonify({"message": f"{product.name} was successfully removed from the order: {order.id}"}), 204


if __name__ == '__main__':
    # Create all tables
    with app.app_context():
        db.create_all()
    # Run the Flask app
    app.run(debug=True)
    # Set the host and port to run the app on
    # app.run(host='
