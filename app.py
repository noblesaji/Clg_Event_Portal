from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


#Create Event Table
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    event_desc = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    event_date = db.Column(db.DateTime, default=datetime.date)
    #reg_deadline = db.Column(db.DateTime, default=datetime.date)

    def __repr__(self):
        return '<Event %r>' % self.id
        

#Create relationships

#Create Students Table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    #password_hash
    #prev_events

    def __repr__(self):
        return '<Student %s>' % self.name



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)