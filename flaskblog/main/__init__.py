import os
import os.path as path
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.models import Hostel, Hostel_Attributes, User
from flaskblog.forms import Hostel_Crud, SearchForm, Hostel_Update, RegisterForm, LoginForm
from flask_login import current_user, login_required, login_user, logout_user