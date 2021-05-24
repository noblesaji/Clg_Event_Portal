from datetime import datetime
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from wtforms.fields.core import IntegerField
from app import login
from app import db

registrants = db.Table('registrants',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class Event(db.Model):
    #__tablename__='events'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50))
    event_body = db.Column(db.String(140))
    event_datetime = db.Column(db.DateTime, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.today)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Event {}>'.format(self.event_name)

class User(UserMixin, db.Model):
    #__tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    events = db.relationship('Event', backref='author', lazy='dynamic')
    registered = db.relationship('Event', secondary=registrants,
                 primaryjoin=(registrants.c.user_id==id),
                 secondaryjoin=(registrants.c.event_id==Event.id),
                 backref=db.backref('registrants',lazy='dynamic'),lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def register(self, event):
        if not self.is_registered(event):
            self.registered.append(event)

    def deregister(self, event):
        if self.is_registered(event):
            self.registered.remove(event)

    def is_registered(self, event):
        return self.registered.filter(registrants.c.event_id == event.id).count() > 0
        
    def registered_events(self):
        return self.registered.order_by(Event.timestamp.desc())

    def __repr__(self):
        return '<User {}>'.format(self.username)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))