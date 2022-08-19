from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

UserGroup = db.Table('UserGroup',
    db.Column('UserID', db.Integer, db.ForeignKey('user.id')),
    db.Column('GroupID', db.Integer, db.ForeignKey('group.id'))
)

class user(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    second_name = db.Column(db.String(150))
    activation_token = db.Column(db.String(150))
    is_activated = db.Column(db.Boolean)

class group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(150))
    is_activated = db.Column(db.Boolean)
    join_token = db.Column(db.String(150))
    users = db.relationship('user', secondary=UserGroup, backref='groups')

