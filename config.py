import os
from dotenv import load_dotenv

base_directory = os.path.abspath(os.path.dirname(__name__))
load_dotenv(os.path.join(base_directory, '.env'))

class Config:
    FLASK_APP=os.getenv('FLASK_APP')
    FLASK_ENV=os.getenv('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY=os.getenv('SECRET_KEY')