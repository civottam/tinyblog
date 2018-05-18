from uuid import uuid4
from os import path
import datetime

from flask import render_template, Blueprint, redirect, url_for, abort
from sqlalchemy import func
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed

from tinyblog.models import db, User, Post, Tag, Comment, posts_tags
from tinyblog.forms import CommentForm, PostForm
from tinyblog.extensions import admin_permission, poster_permission


blog_blueprint = Blueprint('blog', __name__, template_folder=path.join(path.pardir, '/templates', 'blog'), url_prefix='/blog')


def sidebar_data():
    # Get recent posts
    recent = db.session.query(Post).order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(Tag, func.count(posts_tags.c.post_id).label('total')).join(posts_tags).group_by(Tag).order_by('total DESC').limit(5).all()
    return recent, top_tags


@blog_blueprint.route('/')
@blog_blueprint.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, 10)
    recent, top_tags = sidebar_data()
    return render_template('blog/home.html', posts=posts, recent=recent, top_tags=top_tags)


@blog_blueprint.route('/post/<string:post_id>', methods=('GET', 'POST'))
def post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(id=str(uuid4()), name=form.name.data)
        new_comment.text = form.text.data
        new_comment.date = datetime.datetime.now()
        new_comment.post_id = post_id
        db.session.add(new_comment)
        db.session.commit()
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template('blog/post.html', post=post, tags=tags, comments=comments, form=form, recent=recent, top_tags=top_tags)


@blog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template('blog/tag.html', tag=tag, posts=posts, recent=recent, top_tags=top_tags)


@blog_blueprint.route('/user/<string:username>')
def user(username):
    user = db.session.query(User).filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent, top_tags = sidebar_data()
    return render_template('blog/user.html', user=user, posts=posts, recent=recent, top_tags=top_tags)


@blog_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if not current_user:
        return redirect(url_for('main.login'))
    if form.validate_on_submit():
        new_post = Post(id=str(uuid4()), title=form.title.data)
        new_post.text = form.text.data
        new_post.publish_date = datetime.datetime.now()
        new_post.users = current_user
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog.home'))
    return render_template('blog/new_post.html', form=form)


@blog_blueprint.route('/edit/<string:id>', methods=['GET', 'POST'])
@login_required
@poster_permission.require(http_exception=403)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if not current_user:
        return redirect(url_for('main.login'))
    if current_user != post.users:
        return redirect(url_for('blog.post', post_id=id))
    permission = Permission(UserNeed(post.users.id))
    if permission.can() or admin_permission.can():
        form = PostForm()
        if form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            post.publish_date = datetime.datetime.now()
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.post', post_id=post.id))
    else:
        abort(403)
    form.title.data = post.title
    form.text.data = post.text
    return render_template('blog/edit_post.html', form=form, post=post)