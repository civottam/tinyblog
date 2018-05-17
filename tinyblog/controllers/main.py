from os import path
from uuid import uuid4
from flask import Blueprint, flash, redirect, render_template, url_for, request, session

from tinyblog.forms import LoginForm, RegisterForm
from tinyblog.models import db, User
from tinyblog.extensions import twitter


main_blueprint = Blueprint('main', __name__, template_folder=path.join(path.pardir, 'templates', 'main'))

@main_blueprint.route('/')
def index():
    return redirect(url_for('blog.home'))


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("You have been logged in.", category="success")
        return redirect(url_for('blog.home'))
    return render_template('login.html', form=form)


@main_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    flash("You have been logged out.", category="success")
    return redirect(url_for('blog.home'))


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(id=str(uuid4()), username=form.username.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Your user has been created, please login.", category='success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


@main_blueprint.route('/twitter')
def twitter_login():
    return twitter.authorize(callback=url_for('main.twitter_authorized', next=request.args.get('next') or request.referrer or None))


@main_blueprint.route('/twitter-authorized')
@twitter.authorized_handler
def twitter_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    session['twitter_token'] = (resp['oauth_token'], resp['oauth_token_secret'])
    session['twitter_user'] = resp['screen_name']
    user = User.query.filter_by(username=resp['screen_name']).first()
    if user is None:
        user = User(id=str(uuid4()), username=resp['screen_name'], password='twitter')
        db.session.add(user)
        db.session.commit()
    flash('You were signed in as {}.'.format(resp['screen_name']))
    return redirect(next_url)