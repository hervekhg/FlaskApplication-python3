from flask import Flask, render_template
app = Flask(__name__)

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


if __name__ == '__main__':
	app.run(debug=True)