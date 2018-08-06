from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, current_app)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, User
from flaskblog.posts.forms import PostForm
from flaskblog.posts.utils import slugify
from flaskblog.users.utils import send_newpostnotif_email

posts = Blueprint('posts',__name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        post.slug = slugify(form.title.data)

        # Send email notification to all users
        users = User.query.all()
        emailsender = current_app.config['EMAIL_SENDER']
        send_newpostnotif_email(current_user,users,post,emailsender)

        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')

        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/admin/post/all", methods=['GET', 'POST'])
@login_required
def post_all():
    #posts = Post.query.all()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('all_post.html', posts=posts)


@posts.route("/post/<int:post_id>/<slug>")
def post(post_id, slug):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


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
        return redirect(url_for('posts.post', post_id=post.id, slug=post.slug))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user and current_user.username != 'admin237story':
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
