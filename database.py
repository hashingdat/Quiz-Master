# This is useful when you define db = SQLAlchemy() in a separate database.py file and want to use it across multiple files.


from flask_sqlalchemy import SQLAlchemy  #SQLAlchemy, a library that allows Flask to work with relational databases (like SQLite, PostgreSQL, or MySQL).
#SQLAlchemy acts as an ORM (Object-Relational Mapper), meaning you can interact with the database using Python classes instead of raw SQL queries.

db = SQLAlchemy()
#variable db. This db object will be used throughout the project to define models and interact with the database.  It acts as the database connection handler for our Flask app.
# database.py does not create a database immediately.
#   The db object will be used inside app.py like this:
#   db.init_app(app) -----> # This connects the app to the database
