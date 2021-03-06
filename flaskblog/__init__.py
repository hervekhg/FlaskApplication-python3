from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

from flask_marshmallow import Marshmallow

import logging
logging.basicConfig(filename='logs/237story.log', level=logging.INFO)


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
ma = Marshmallow()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    ma.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.roles.routes import roles
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(roles)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app