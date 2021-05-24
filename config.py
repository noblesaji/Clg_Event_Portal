import os
basedir = os.path.abspath(os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or str(os.getenv('SECRET_KEY'))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL?sslmode=require').replace('postgres://', 'postgresql://') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False