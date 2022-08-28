from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

UserGroup = db.Table('UserGroup',
    db.Column('UserID', db.Integer, db.ForeignKey('user.id')),
    db.Column('GroupID', db.Integer, db.ForeignKey('group.id')),
)

GroupAdmins = db.Table('GroupAdmins',
    db.Column('UserID', db.Integer, db.ForeignKey('user.id')),
    db.Column('GroupID', db.Integer, db.ForeignKey('group.id')),
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
    token = db.Column(db.String(150))
    users = db.relationship('user', secondary=UserGroup, backref='groups')
    adminusers = db.relationship('user', secondary=GroupAdmins, backref='groupsIsAdmin')
    assets = db.relationship('assets', backref='assetgroup')

class assets(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    asset_name = db.Column(db.String(150))
    is_activated = db.Column(db.Boolean)
    type = db.Column(db.String(150))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    bookings = db.relationship('bookings', backref='asset')

class booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    asset_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    starttime = db.Column(db.DateTime)
    endtime = db.Column(db.DateTime)
