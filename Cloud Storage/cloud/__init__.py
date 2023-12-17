from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ngrok import run_with_ngrok

app = Flask(__name__)

run_with_ngrok(app)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 50 * 1000 * 1000
db = SQLAlchemy(app)