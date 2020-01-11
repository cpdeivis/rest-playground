from playground.ext.database import db
from datetime import datetime
import enum


class AuthorType(enum.Enum):
    A = 'Admin'
    R = 'Reader'
    W = 'Writer'


class UpdateMixin:
    def update(self, values):
        for k, v in values.items():
            try:
                setattr(self, k, v)
            except:
                continue


class Author(db.Model, UpdateMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=False, nullable=False)
    type = db.Column(db.Enum(AuthorType), index=False, nullable=False, default='R')

    def __repr__(self):
        return '<Author %r>' % self.name


class ToDo(db.Model, UpdateMixin):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship('Author', backref=db.backref('todos', lazy=True))
    created = db.Column(db.Date, nullable=True, default=datetime.utcnow().date())

    def __repr__(self):
        return '<ToDo %r>' % self.id