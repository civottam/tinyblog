# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

from main import app

# INIT the sqlalchemy object                            
# Will be load the SQLALCHEMY_DATABASE_URL from config.py
# SQLAlchemy will load configuration defined in DevConfig from APP object
db = SQLAlchemy(app)


class User(db.Model):
    """Blog users."""

    # Table initialization
    __tablename__ = 'users'
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    # Establish contact with Post's ForeignKey: user_id
    posts = db.relationship('Post', backref='users', lazy='dynamic')

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    def __repr__(self):
        """Define the string format for instance of User."""
        return "<Model User `{}`>".format(self.username)


# Create relationship table between Tag and Post
posts_tags = db.Table('posts_tags', 
                    db.Column('post_id', db.String(45), db.ForeignKey('posts.id')), 
                    db.Column('tag_id', db.String(45), db.ForeignKey('tags.id'))
                )

class Post(db.Model):
    """Posts of users."""

    __tablename__ = 'posts'
    id = db.Column(db.String(45), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_date = db.Column(db.DateTime)
    # Set foreign key of Post
    user_id = db.Column(db.String(45), db.ForeignKey('users.id'))
    # Establish contact with Comment's foriegn key; post_id
    comments = db.relationship('Comment', backref='posts', lazy='dynamic')
    # many to many, posts <==> tags
    tags = db.relationship('Tag', secondary=posts_tags, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, id, title):
        self.id = id
        self.title = title

    def __repr__(self):
        return "<Model Post `{}`>".format(self.title)


class Comment(db.Model):
    """Comments of each post."""

    __tablename__ = 'comments'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    date = db.Column(db.DateTime)
    # Set foreign key of Comment
    post_id = db.Column(db.String(45), db.ForeignKey('posts.id'))

    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return "<Model Comment `{}`>".format(self.name)


class Tag(db.Model):
    """Tags of each post."""

    __tablename__ = 'tags'
    id = db.Column(db.String(45), primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return "<Model Tag `{}`>".format(self.name)