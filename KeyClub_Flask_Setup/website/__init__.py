#initiation file for website, ran on import
from flask import Flask
import website.fetching
from website.config import *

app = Flask(__name__)

from .views import views

app.register_blueprint(views, url_prefix="/")
app.jinja_env.filters['zip'] = zip
app.config["SECRET_KEY"] = SECRET_KEY


app.config["PROPAGATE_EXCEPTIONS"] = True