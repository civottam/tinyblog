from flask import Flask, redirect, url_for
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed
from sqlalchemy import event

from tinyblog.models import db, Reminder
from tinyblog.controllers import blog, main
from tinyblog.extensions import bcrypt, login_manager, principals, flask_celery_helper
from tinyblog.tasks import on_reminder_save


def create_app(object_name):
    """To create app instance with factory method"""
    app = Flask(__name__)
    app.config.from_object(object_name)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    flask_celery_helper.init_app(app)
    event.listen(Reminder, 'after_insert', on_reminder_save)

    # This function will receive signal sent by 'identity_changed.send' in controller.main, the signal includes identity of user object in 
    # app object was changed, then the function will grant permission to user by binding Needs to user.
    # After user authentication is passed successfully, Flask-Principal will save user's identity object into session.
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        identity.user = current_user
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
        if hasattr(current_user, 'roles'):
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.name))

    @app.route('/')
    def index():
        return redirect(url_for('blog.home'))
    
    app.register_blueprint(blog.blog_blueprint)
    app.register_blueprint(main.main_blueprint)
    
    return app