from flask import (render_template, url_for, flash,
                   redirect, request, jsonify, abort, Blueprint, current_app)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, User, PostSchema
from flaskblog.posts.forms import PostForm
from flaskblog.posts.utils import slugify
from flaskblog.users.utils import send_newpostnotif_email


import threading
import datetime

#Pour debug
import sys


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
        db.session.add(post)

        try:
            db.session.commit()
            flash('Your post has been created!', 'success')
            current_app.logger.info("New Story - %s", (current_user.username, current_user.email, post.slug))
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
def post(slug):
    #post = Post.query.get_or_404(post_id)
    #return render_template('post.html', title=post.title, post=post)
    post = Post.query.filter(Post.slug==slug).first()

    post_id = int(post.id)
    post_id_prev = post_id + 1
    post_id_suiv = post_id - 1

    #prev_image = Post.query.order_by(id.desc()).filter(Images.id < id).first()

    prev = (Post.query.order_by(Post.id.desc()).filter(Post.id < post_id).first())
    suiv = (Post.query.order_by(Post.id.asc()).filter(Post.id > post_id).first())
    
    if prev is not None:
        slug_prev = prev.slug
    else:
        slug_prev = slug

    if suiv is not None:
        slug_suiv = suiv.slug
    else:
        slug_suiv = slug

    current_app.logger.info("URI: - %s", (post.slug))
    return render_template('post.html', title=post.title, post=post, slug_suiv=slug_suiv, slug_prev=slug_prev)


@posts.route("/search", methods=['GET', 'POST'])
def search():
    keyword = request.args.get("search")
    find_keyword = "%" + keyword + "%"
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.title.like(find_keyword)).order_by(Post.date_posted.desc()).paginate(page=page, per_page=20)
    current_app.logger.info("New Search - %s", (find_keyword))

    current_app.logger.info("FIND: - %s", (keyword))
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
        current_app.logger.info("Update Story - %s", (current_user.username, current_user.email, post.slug))
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
    current_app.logger.info("New Delete - %s", (current_user.username, current_user.email, post.slug))
    return redirect(url_for('posts.post_all'))


@posts.route("/post/notification", methods=['GET','POST'])
@login_required
def sendemail_post():
    today = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    yesterday = str(datetime.datetime.now() - datetime.timedelta(days = 1))
    
    if current_user.username != 'admin237story':
        abort(403)
    # Send email notification to all users
    users = User.query.all()
    posts = Post.query.filter(Post.date_posted.between(yesterday, today)).order_by(Post.date_posted.desc())
    emailsender = current_app.config['EMAIL_SENDER']
    username = current_user.username
    send_newpostnotif_email(username,users,posts,emailsender)
    flash('The email notification has been sent!', 'success')
    current_app.logger.info("New Notification - %s", (current_user.username, current_user.email))
    return redirect(url_for('main.home'))

@posts.route("/post/like/<int:post_id>", methods=['GET','POST'])
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.like_post is None:
        post.like_post = 1
    else:
        post.like_post = post.like_post + 1
    db.session.commit()
    current_app.logger.info("New Like - %s", (post.slug))
    return redirect(url_for('posts.post',post_id=post.id, slug=post.slug))

@posts.route("/post/dislike/<int:post_id>", methods=['GET','POST'])
def dislike_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.dislike_post is None:
        post.dislike_post = 1 
    else:
        post.dislike_post = post.dislike_post + 1
    db.session.commit()
    current_app.logger.info("New DisLike - %s", (post.slug))
    return redirect(url_for('posts.post',post_id=post.id, slug=post.slug))


@posts.route("/politic")
def politic():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.title.like("%politique%")).order_by(Post.date_posted.desc()).paginate(page=page, per_page=20)
    return render_template('home.html', posts=posts)

@posts.route("/economy")
def economy():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.title.like("%economie%")).order_by(Post.date_posted.desc()).paginate(page=page, per_page=20)
    return render_template('home.html', posts=posts)

@posts.route("/sport")
def sport():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.title.like("%sport%")).order_by(Post.date_posted.desc()).paginate(page=page, per_page=20)
    return render_template('home.html', posts=posts)

@posts.route("/education")
def education():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.title.like("%education%")).order_by(Post.date_posted.desc()).paginate(page=page, per_page=20)
    return render_template('home.html', posts=posts)

@posts.route("/others")
def divers():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.title.like("%divers%")).order_by(Post.date_posted.desc()).paginate(page=page, per_page=20)
    return render_template('home.html', posts=posts)

##------------------------------------------------------------------------------------------
# API ENDPOINT URL #
#-------------------------------------------------------------------------------------------
@posts.route("/api/post/all", methods=['GET'])
def api_post_all():
    current_app.logger.info("New Mobile Call - GET ALL POST")
    allposts = Post.query.order_by(Post.date_posted.desc()).limit(250).all()
    posts_schema = PostSchema(many=True)
    result = posts_schema.dump(allposts)
    return jsonify(result.data)


@posts.route("/api/post/politic", methods=['GET'])
def api_post_politic():
    current_app.logger.info("New Mobile Call - GET POLITIC POST")
    allposts = Post.query.filter(Post.title.like("%politique%")).order_by(Post.date_posted.desc()).limit(250).all()
    posts_schema = PostSchema(many=True)
    result = posts_schema.dump(allposts)
    return jsonify(result.data)

@posts.route("/api/post/economy", methods=['GET'])
def api_post_economic():
    current_app.logger.info("New Mobile Call - GET ECONOMIC POST")
    allposts = Post.query.filter(Post.title.like("%economie%")).order_by(Post.date_posted.desc()).limit(250).all()
    posts_schema = PostSchema(many=True)
    result = posts_schema.dump(allposts)
    return jsonify(result.data)

@posts.route("/api/post/sport", methods=['GET'])
def api_post_sport():
    current_app.logger.info("New Mobile Call - GET SPORT POST")
    allposts = Post.query.filter(Post.title.like("%sport%")).order_by(Post.date_posted.desc()).limit(250).all()
    posts_schema = PostSchema(many=True)
    result = posts_schema.dump(allposts)
    return jsonify(result.data)

@posts.route("/api/post/education", methods=['GET'])
def api_post_education():
    current_app.logger.info("New Mobile Call - GET EDUCATION POST")
    allposts = Post.query.filter(Post.title.like("%education%")).order_by(Post.date_posted.desc()).limit(250).all()
    posts_schema = PostSchema(many=True)
    result = posts_schema.dump(allposts)
    return jsonify(result.data)

@posts.route("/api/post/biya", methods=['GET'])
def api_post_biya():
    current_app.logger.info("New Mobile Call - GET BIYA POST")
    allposts = Post.query.filter(Post.title.like("%biya%")).order_by(Post.date_posted.desc()).limit(250).all()
    posts_schema = PostSchema(many=True)
    result = posts_schema.dump(allposts)
    return jsonify(result.data)

@posts.route("/api/post/kamto", methods=['GET'])
def api_post_kamto():
    current_app.logger.info("New Mobile Call - GET KAMTO POST")
    allposts = Post.query.filter(Post.title.like("%kamto%")).order_by(Post.date_posted.desc()).limit(250).all()
    posts_schema = PostSchema(many=True)
    result = posts_schema.dump(allposts)
    return jsonify(result.data)

@posts.route("/api/post/libii", methods=['GET'])
def api_post_libii():
    current_app.logger.info("New Mobile Call - GET LIBII POST")
    allposts = Post.query.filter(Post.title.like("%libii%")).order_by(Post.date_posted.desc()).limit(250).all()
    posts_schema = PostSchema(many=True)
    result = posts_schema.dump(allposts)
    return jsonify(result.data)

@posts.route("/api/post/divers", methods=['GET'])
def api_post_divers():
    current_app.logger.info("New Mobile Call - GET FAIT DIVERS POST")
    allposts = Post.query.filter(Post.title.like("%divers%")).order_by(Post.date_posted.desc()).limit(250).all()
    posts_schema = PostSchema(many=True)
    result = posts_schema.dump(allposts)
    return jsonify(result.data)

@posts.route("/api/post/noso", methods=['GET'])
def api_post_noso():
    current_app.logger.info("New Mobile Call - GET NOSO POST")
    allposts = Post.query.filter(Post.title.like("%noso%")).order_by(Post.date_posted.desc()).limit(250).all()
    posts_schema = PostSchema(many=True)
    result = posts_schema.dump(allposts)
    return jsonify(result.data)