
# Relational Databases & API Rest Development Project: Building an E-Commerce API

Project Overview
In this assignment, you will create a fully functional e-commerce API using Flask, Flask-SQLAlchemy, Flask-Marshmallow, and MySQL. The API will manage Users, Orders, and Products with proper relationships, including One-to-Many and Many-to-Many associations. You will also learn to set up a MySQL database, define models, implement serialization with Marshmallow, and develop RESTful CRUD endpoints.

✨ Learning Objectives
By the end of this project, students will be able to:
✅ Database Design: Create models with relationships in SQLAlchemy and MySQL.
✅ API Development: Develop a RESTful API with CRUD operations using Flask.
✅ Serialization: Use Marshmallow schemas for input validation and data serialization.
✅ Testing: Ensure the API is fully functional using Postman and MySQL Workbench.


MySQL Workbench was used to create a LocalHost server connection for the Database. 

A Virtual Environment was used with specific packages. Follow the below instructions:

In Visual Studio Code Terminal create a virtual environment (Windows): py -m venv venv

Activate the virtual environment:
\venv\Scripts\Activate

In the Terminal you should see (venv) on the left side of the terminal.

Install the packages from the requirements.txt file:
pip install -r requirements.txt

Database was coded/created using Python in Visual Studio Code with a SQLAlchemy_Database_URI linking to the MySQL Workbench server connection database.

POSTMAN was used for creating API Requests to test the Database at https://www.postman.com/

Database contains:
User Table: id, name, address, email
Order Table: id, order_date, user_id
Product Table: id, product_name, price
Order_Product Association Table: order_id, product_id

CRUD Endpoints:
User Endpoints
    GET /users: Retrieve all users
    GET /users/<id>: Retrieve a user by ID
    POST /users: Create a new user
    PUT /users/<id>: Update a user by ID
    DELETE /users/<id>: Delete a user by ID
Product Endpoints
    GET /products: Retrieve all products
    GET /products/<id>: Retrieve a product by ID
    POST /products: Create a new product
    PUT /products/<id>: Update a product by ID
    DELETE /products/<id>: Delete a product by ID
Order Endpoints
    POST /orders: Create a new order (requires user ID and order date)
    PUT /orders/<order_id>/add_product/<product_id>: Add a product to an order (prevent duplicates)
    DELETE /orders/<order_id>/remove_product: Remove a product from an order
    GET /orders/user/<user_id>: Get all orders for a user
    GET /orders/<order_id>/products: Get all products for an order

Programming Languges:
Python


## Authors

- [@GeoffreyBurt](https://github.com/GJBURT)


## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/geoffreyjburt/)

[![github](https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/GJBURT)

