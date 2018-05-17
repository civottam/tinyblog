from flask_bcrypt import Bcrypt
from flask_oauth import OAuth
from flask import session

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