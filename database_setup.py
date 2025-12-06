# This script will initialize the database and create tables.

#from app import app   #This loads the Flask application.
from database import db
from flask import Flask
from models import User, Subject, Chapter, Quiz, Question, Option, Scores 



def initialize_database(app):
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin exists, if not create one
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin_user = User(
                username='admin',
                email='admin@quizmaster.com',
                password='admin123',  # In production, you should hash this
                role='admin'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created!")
        
        print("Database initialized successfully!")

