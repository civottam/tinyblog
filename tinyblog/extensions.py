from flask import session
from flask_bcrypt import Bcrypt
from flask_oauth import OAuth
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_celery import Celery
from flask_mail import Mail

# Flask-Bccrypt initialization
bcrypt = Bcrypt()

# Flask-OAuth initialization
oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize',
    consumer_key='<public_key>',
    consumer_secret='<private_key>'
)

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

# Flask-login intialization
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please login to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from tinyblog.models import User
    return User.query.filter_by(id=user_id).first()

# Flask-Principal initialization
principals = Principal()
admin_permission = Permission(RoleNeed('admin'))
poster_permission = Permission(RoleNeed('poster'))
default_permission = Permission(RoleNeed('default'))

# Flask-Celery-helper initialization
flask_celery_helper = Celery()

# Flask-Mail initialization
mail = Mail()