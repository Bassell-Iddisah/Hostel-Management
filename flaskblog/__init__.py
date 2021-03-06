from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flaskblog.config import Config


app = Flask(__name__)
app.config['SECRET_KEY'] = '5e94b5bebf323cbffbaae873e32df4c137e9a2b1ef80b705566321706e3e47e7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
PORT = 5000
bcrypt = Bcrypt(app)
migrate = Migrate(app)

from flaskblog.main.routes import main
from flaskblog.hostel.routes import hostel
from flaskblog.user.routes import user

app.register_blueprint(main)
app.register_blueprint(hostel)
app.register_blueprint(user)


# Replace hostel_layout menu with hostel_page navigation