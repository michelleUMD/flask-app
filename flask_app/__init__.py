# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime
import os

# local
from .client import PackageClient

from flask_talisman import Talisman


db = MongoEngine()
login_manager = LoginManager()
bcrypt = Bcrypt()
package_client = PackageClient()

from .routes import main

from .users.routes import users
from .packages.routes import packages


def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    csp = {
        'default-src': [
            '\'self\'',
            'stackpath.bootstrapcdn.com',
            'code.jquery.com',
            'cdn.jsdelivr.net'
        ]
    }
    Talisman(app, content_security_policy=csp)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(packages) 
    app.register_blueprint(users) 

    app.register_error_handler(404, page_not_found)

    login_manager.login_view = "users.login"

    app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST")
    
    return app
