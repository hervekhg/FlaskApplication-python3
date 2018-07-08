from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post

posts = [

   {
   		'author': 'Herve Gaël',
   		'title': 'Histoire Blog',
   		'content' : 'First post content',
   		'date_posted' : 'Juillet 2018'

   },

   {
   		'author': 'Isabelle',
   		'title': 'Histoire bretonne',
   		'content' : 'Second Post',
   		'date_posted' : 'Juillet 2018'

   }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html",title='About')


@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
    	flash(f'Account created for { form.username.data }!','success')
    	return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
    	if form.email.data == 'hervekhg@gmail.com' and form.password.data == 'test':
    		flash('You have been logged in','success')
    		return redirect(url_for('home'))
    	else:
    		flash('Login unsuccesful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


