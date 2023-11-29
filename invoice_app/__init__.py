import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:9mobile@localhost:5432/lecture1'



db = SQLAlchemy(app)
db.create_all()
db.session.commit()
# Set up database
app.secret_key = 'iamasecretkey'
if __name__ == "__main__":
    app.run()