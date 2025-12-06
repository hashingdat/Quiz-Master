
# this file contain all the database model(table)
# A model in Flask-SQLAlchemy represents a table in the database.
# Each class(user, scores,subject , chatper etc.) in models.py corresponds to a table.
# Each attribute(id,username , paswrod etc.) in a class corresponds to a column in that table.



from database import db
from flask_login import UserMixin #User authentication aur session management ke liye use hota hai.


# ✅ In short:
# SQLite is the database.
# SQLAlchemy is a Python tool that helps you work with SQLite (and other databases),by allowing python function to write sql quereid and not using hetic raw sql

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin' or 'user'
# db.Model is a special class provided by SQLAlchemy.
# When we use db.Model, Flask-SQLAlchemy automatically:
# Creates a database table (User table in this case).
# Maps the class attributes (id, username, etc.) to table columns.
# Allows us to interact with the table using Python instead of SQL.

#----------->in simple words--->database table banane and interact krne ke kaam ata hai
#  Without db.Model --->(Raw SQL Approach)
#with db.model----->You can use Python functions to interact with the database.
   
    def set_password(self, password):
        self.password = password      #Without self, Python wouldn’t know which object's data to access.

    def check_password(self, password):
        return self.password == password


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    chapters = db.relationship('Chapter', backref='subject', lazy=True)
#dont get confuse with chapters(simple variable name   ------ that stores the relationship between Subject and Chapter.) and chatper(class)
#db.relationship ------> 1 to many relaitonship------> one subject can have many chapter

#  backref ----> creates a reverse connection from Chapter to Subject.
#  This means [you can access the parent Subject from a Chapter ] without defining another relationship in the Chapter model.
# example chapter = Chapter.query.first()
# print(chapter.subject.name)  --------->Thanks to backref, we can access subject directly

#lazy=true -----> Loads chapters only when needed (memory efficient)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True)
    def __repr__(self):
        return f'<Chapter {self.name}>'

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    questions = db.relationship('Question', backref='quiz', lazy=True)
    time_duration = db.Column(db.Integer, nullable=False, default=10)  # in minutes

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)
    options = db.relationship('Option', backref='question', lazy=True, foreign_keys='Option.question_id')
  #  correct_option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=True)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    option_text = db.Column(db.String(200), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    answers = db.relationship('UserAnswer', backref='score', cascade='all, delete-orphan')


class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score_id = db.Column(db.Integer, db.ForeignKey('scores.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_option = db.Column(db.String(1), nullable=False)  # 'A', 'B', etc.
    is_correct = db.Column(db.Boolean, nullable=False)




if __name__ == "__main__":
    db.create_all()      #This creates all tables(models) defined in models.py inside the database.

# This condition checks whether the script is being run directly or imported as a module.
# If the script is executed directly (python file.py), the code inside this block will run.
# else --> if the script is imported into another Python file, the block will not execute.    