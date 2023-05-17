from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_msearch import Search

app = Flask(__name__)

app.config['SECRET_KEY'] = '665effa02d70007ef16b81c5a369cda8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = "static/laptop_pics"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
search = Search()
search.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tobikyle28@gmail.com'
app.config['MAIL_PASSWORD'] = 'hxliywaxsefsdtwo'
mail = Mail(app)

from store import routes