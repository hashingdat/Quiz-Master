import os   #We need it to define file paths dynamically, ensuring cross-platform compatibility.
from datetime import timedelta


BASE_DIR = os.path.abspath(os.path.dirname(__file__)) #It gets the absolute path ---> so that database file is correclt stored
#abspath meaning abouslute path (full path)
#os.path.dirname-----> gets the directory where config.py is
#__file__ ----> special built in python variable

class Config:
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.getcwd(), 'instance', 'quiz_master.sqlite3')}'
    #URI (Uniform Resource Identifier) is a string that uniquely identifies a resource, like a database or a file location.
    #sqlite:///--->This tells Flask-SQLAlchemy to use SQLite as the database. The /// means that the database is stored as a file (not a server-based DB like PostgreSQL or MySQL).  
#Other Examples of Database URIs
#Database Type	URI Format
#SQLite	sqlite:///relative/path.db or sqlite:////absolute/path.db
#PostgreSQL	postgresql://user:password@localhost/dbname
#MySQL	mysql+pymysql://user:password@localhost/dbname 
    SQLALCHEMY_TRACK_MODIFICATIONS = False  #improves and save memory



SECRET_KEY = 'dev-key-123'    #Enables Sessions: Required for using session in Flask. and
#secret is must for login users and admin
PERMANENT_SESSION_LIFETIME = timedelta(days=7)