from flask import Flask, redirect, url_for, jsonify
from config import Config
from database import db
from models import Chapter, Quiz, Scores, Subject, User 
from flask_migrate import Migrate
#from routes.user_routes import user_bp

from flask_login import LoginManager
from routes.auth_routes import register_routes  #from routes folder auth_roles importing the funtion refister_routes
from routes.auth_routes import register_dashboard_routes
from routes.admin_routes import init_admin_routes
from routes.user_routes import init_user_routes 

from database_setup import initialize_database


app = Flask(__name__, template_folder='templates')#Creates an instance of the Flask application. #tell the flask that this script is the starting point of the web app
                     #__name__ ------> special inbuilt variable helps Flask determine the correct root directory of the application.print("[DEBUG] Right after creation - Secret key exists?", hasattr(app, 'secret_key'))

app.secret_key='12345' #use for session management of users and admin

app.config.from_object(Config)  #Loads the configuration settings from config.py
#app.register_blueprint(user_bp)

db.init_app(app) #Initializes the database connection with the Flask app.------->tells Flask how to connect to the database using SQLAlchemy.
#It binds the database to the Flask app, allowing you to interact with the database.
migrate = Migrate(app, db)


# API Endpoint to get all subjects
@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    subjects_list = [{
        'id': subject.id,
        'name': subject.name
    } for subject in subjects]
    return jsonify(subjects_list)

# API Endpoint to get chapters 
@app.route('/api/subjects/<int:subject_id>/chapters', methods=['GET'])
def get_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    chapters_list = [{
        'id': chapter.id,
        'name': chapter.name,
        'subject_id': chapter.subject_id
    } for chapter in chapters]
    return jsonify(chapters_list)


# API Endpoint to get all quizzes for a specific chapter
@app.route('/api/chapters/<int:chapter_id>/quizzes', methods=['GET'])
def get_quizzes(chapter_id):
    quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
    
    quizzes_list = [{
        'id': quiz.id,
        'title': quiz.title,
        'time_duration': quiz.time_duration,
        'chapter_id': quiz.chapter_id
    } for quiz in quizzes]
    
    return jsonify(quizzes_list)

# API Endpoint to get detailed information for a specific quiz


login_manager = LoginManager() #Creates an instance of LoginManager, which manages user authentication.
login_manager.init_app(app) # links user authentication with the flask application.
login_manager.login_view = 'login' #Specifies the login page route.---->Agar koi protected route ko direct acces krne ka try karega then flask-login usko redirect krega /login pe ---> security.


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


initialize_database(app)

register_routes(app)  #from routes folder auth_roles importing the funtion refister_routes  ---->  #function to Register wale Routes 
register_dashboard_routes(app)  #for the user dashbaord route
init_admin_routes(app, db)
init_user_routes(app, db)

@app.route('/')
def home():
    return redirect(url_for('register'))


if __name__ == "__main__":
    app.run(debug=True)



   # initialize_database() #jab run karenge toh firstly app.run hoga and initialize_database hoga
                          #initialize_databse --->>>database ke tables create honge and admin predefine hoha  


# Python mein har ek file ka ek naam (__name__) hota hai. Jab tum kisi file ko directly run karte ho, toh uska naam "__main__" hota hai.
#  "Direct run" ka matlab hai python app.py chalana.
#  "Import as module" ka matlab hai us file ko kisi aur file mein use karna.
#  if __name__ == "__main__": sirf tabhi chalega jab file ko directly run karoge.    



# IMpoertant order :
# app = Flask(__name__)          Create app
# app.config.from_object(Config)  Load config
# db.init_app(app)                Initialize extensions
# register_routes(app)          Register routes