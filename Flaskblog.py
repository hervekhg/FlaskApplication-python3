from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'f334629b7e141f50f5edb664e038ccf4'

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

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)



if __name__ == '__main__':
	app.run(debug=True)