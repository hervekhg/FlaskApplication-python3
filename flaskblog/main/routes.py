from flask import render_template, request, Blueprint, current_app, make_response, url_for
from flaskblog.models import Post
from datetime import datetime, timedelta, time, date

main = Blueprint('main',__name__)

@main.route("/")

@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=20)
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/sitemap.xml",methods=['GET'])
def sitemap_xml():
	"""Generate sitemap.xml. Makes a list of urls and date modified."""
	pages=[]
	ten_days_ago=datetime.now() - timedelta(days=10)
	ten_days_ago=ten_days_ago.strftime('%Y-%m-%d')
	# static pages
	# for rule in current_app.url_map.iter_rules():
	# 	if "GET" in rule.methods and len(rule.arguments)==0:
	# 		pages.append([rule.rule,ten_days_ago])
	for url in ['main.home', 'main.about']:
		page = url_for(url, _external=True)
		pages.append([page,ten_days_ago])

	posts = Post.query.order_by(Post.date_posted.desc())
	for post in posts:
		page = url_for('posts.post', slug=post.slug, _external=True)
		pages.append([page,ten_days_ago])

	sitemap_xml = render_template('sitemap/sitemap_template.xml', pages=pages)
	response= make_response(sitemap_xml)
	response.headers["Content-Type"] = "application/xml"    
	return response

@main.route("/robots.txt")
def robots_txt():
    return render_template("robots.txt")