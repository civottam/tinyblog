from flask import session
from flask_bcrypt import Bcrypt
from flask_oauth import OAuth
from flask_login import LoginManager


bcrypt = Bcrypt()

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


login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'
login_manager.login_message = 'Please login to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from tinyblog.models import User
    return User.query.filter_by(id=user_id).first()