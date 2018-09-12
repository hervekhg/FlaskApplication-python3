from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, current_app)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, User
from flaskblog.posts.forms import PostForm
from flaskblog.posts.utils import slugify
from flaskblog.users.utils import send_newpostnotif_email

import threading

posts = Blueprint('posts',__name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        post.slug = slugify(form.title.data)
        post.like_post = 0
        post.dislike_post = 0
        # Send email notification to all users
        users = User.query.all()
        emailsender = current_app.config['EMAIL_SENDER']
        username = current_user.username
        send_newpostnotif_email(username,users,post,emailsender)
        
        db.session.add(post)
        try:
            db.session.commit()
            flash('Your post has been created!', 'success')
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()

        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Story')


@posts.route("/admin/post/all", methods=['GET', 'POST'])
@login_required
def post_all():
    #posts = Post.query.all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('all_post.html', posts=posts)


#@posts.route("/post/<int:post_id>/<slug>")
@posts.route("/<slug>")
#@login_required
#def post(post_id, slug):
def post(slug):
    #post = Post.query.get_or_404(post_id)
    #return render_template('post.html', title=post.title, post=post)
    post = Post.query.filter(Post.slug==slug).first()
    return render_template('post.html', title=post.title, post=post)

@posts.route("/search", methods=['GET', 'POST'])
def search():
    keyword = request.args.get("search")
    find_keyword = "%" + keyword + "%"
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.title.like(find_keyword)).order_by(Post.date_posted.desc()).paginate(page=page, per_page=20)
    return render_template('search.html', posts=posts)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.username != 'admin237story':
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', slug=post.slug))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    #post = Post.query.get_or_404(post_id)
    post = Post.query.filter_by(id=post_id).first()
    if post.author != current_user and current_user.username != 'admin237story':
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))


@posts.route("/post/like/<int:post_id>", methods=['GET','POST'])
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.like_post is None:
        post.like_post = 1
    else:
        post.like_post = post.like_post + 1
    db.session.commit()
    return redirect(url_for('posts.post',post_id=post.id, slug=post.slug))

@posts.route("/post/dislike/<int:post_id>", methods=['GET','POST'])
def dislike_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.dislike_post is None:
        post.dislike_post = 1 
    else:
        post.dislike_post = post.dislike_post + 1
    db.session.commit()
    return redirect(url_for('posts.post',post_id=post.id, slug=post.slug))

