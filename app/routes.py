from threading import currentThread
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app
from app import db
from app.forms import LoginForm, SignUpForm, EventForm
from app.models import User, Event
from datetime import datetime

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():
    my_events = current_user.registered_events().all()
    all_events = Event.query.order_by(Event.timestamp.desc()).all()
    return render_template('index.html', title='Home Page', my_events=my_events, all_events=all_events)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! You are now a registered user.')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form=EventForm()
    if form.validate_on_submit():
        event = Event(event_name=form.event_name.data, 
                event_body=form.event_body.data, 
                event_datetime=form.event_datetime.data, 
                author=current_user)
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!')
        return redirect(url_for('index'))
    return render_template('create.html', title='Create Event', form=form)


@app.route('/event/<event_name>', methods=['GET', 'POST'])
@login_required
def event(event_name):
    event = Event.query.filter_by(event_name=event_name).first_or_404()
    if request.method == 'POST':
        if request.form.get('register') == 'Register for Event':
            current_user.register(event)
            db.session.commit()
            flash("You have been registered for "+event_name)
            return redirect(url_for('index'))
        elif request.form.get('deregister') == 'Revoke Registration for Event':
            current_user.deregister(event)
            db.session.commit()
            flash("Your registration for "+event_name+" has been revoked")
            return redirect(url_for('index'))
        elif request.form.get('delete') == 'Delete Event':
            db.session.delete(event)
            db.session.commit()
            flash('Your event has been deleted.')
            return redirect(url_for('index'))
    return render_template('event.html', title='Event: '+event_name, event=event)
    

