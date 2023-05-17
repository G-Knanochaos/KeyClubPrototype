#initiation file for website, ran on import
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from sqlalchemy.pool import StaticPool

db = SQLAlchemy()
app = Flask(__name__)
DB_NAME= "user_database.db"

app.config['SECRET_KEY'] = 'Your mother is hawt'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from .models import User

if not path.exists('website/' + DB_NAME):
    with app.app_context():
        db.create_all()
        print('Created Database!')

from .views import views
from .auth import auth

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(auth, url_prefix="/")

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
