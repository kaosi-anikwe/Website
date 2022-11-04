from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from models import Users
from dotenv import load_dotenv
import os

load_dotenv()

# get remote db URI from environment variables
remote_db = os.getenv("REMOTE_DB")

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://ba9ae764e59af3:834d6bc9@us-cdbr-east-04.cleardb.com" \
    # "/heroku_a0fdeca9b5d4d8d"
    app.config["SQLALCHEMY_DATABASE_URI"] = remote_db
    app.config['SECRET_KEY'] = "secret"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 60

    login_manager.login_view = "auth.signin"
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app