from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# initialises flask application
app = Flask(__name__)

# adds database functionality
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

from v1 import book_route