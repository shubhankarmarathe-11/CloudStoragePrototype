from cloud import db,app
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_login import UserMixin
from datetime import datetime


class User(db.Model,UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String,nullable=False)
    data = db.relationship('Upload', backref='User', lazy=True)

class Upload(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(5000),nullable=False)
    data = db.Column(db.LargeBinary,nullable=False)
    date: Mapped[str] = mapped_column(db.DateTime,default=datetime.utcnow)
    owned_user = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

with app.app_context():
    db.create_all()