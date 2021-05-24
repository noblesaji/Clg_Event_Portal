from datetime import datetime, date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators
from wtforms.fields.core import DateTimeField
from wtforms.fields.html5 import DateField, TimeField, DateTimeLocalField, DateTimeField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, NoneOf, ValidationError, Email, EqualTo
from wtforms_components import DateRange
from app.models import User, Event

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different e-mail address.')


class EventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired(), Length(min=1, max=100)])
    event_body = TextAreaField('Description of Event', validators=[DataRequired()])
    event_datetime = DateField('Date of Event', validators=[DataRequired()])
    #event_time = TimeField('Time of Event', validators=[InputRequired()])
    submit = SubmitField('Create Event')

    '''def validate_event_datetime(self, event_datetime):
        if event_datetime not in DateRange(min=datetime.now):
            raise ValidationError("The date cannot be in the past!")'''

    def validate_event_name(self, event_name):
        event_name = Event.query.filter_by(event_name=event_name.data).first()
        if event_name is not None:
            raise ValidationError("This event already exists")