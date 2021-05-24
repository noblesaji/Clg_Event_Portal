import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '@eELZQbuxUPc!EQN2K-wJjcquC+??%2YpC-Grr#6D*usmMg&UM5XYAm#wKFW@wW%K=Ge&*wnSXZ#7Pn8QPvdn*x*gk^X&PVy6TD9mYYTuAQ*_?8-!2&KwzYxRa^G2@6DsP^dpzrxJLUZBbBAN8_a4XUV_pWe&8KJhSP*J%Q%YtjDMyHA3%+A9f-^PTVZVz*ZHttLJcfZNrLD$@4#Q^?fnKPq&L&5eD9Dt6J%katGgEJayB4!3V+v?vhQShtMTSnd'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False