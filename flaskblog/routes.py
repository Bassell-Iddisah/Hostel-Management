import os
import os.path as path
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.models import Hostel, Hostel_Attributes, User
from flaskblog.forms import Hostel_Crud, SearchForm, Hostel_Update, RegisterForm, LoginForm
from flask_login import current_user, login_required, login_user, logout_user


# ####################################################Core Routes ###
@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
    searchform = SearchForm()
    all_hostels = Hostel.query.all()
    if searchform.validate_on_submit():
        query = searchform.search_input.data
        return redirect(url_for('search_results', query=query))
    return render_template("home.html", title='Home', searchform=SearchForm(), current_user=current_user, hostels=all_hostels)


@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About Us', searchform=SearchForm())


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    all_hostels = Hostel.query.all()
    return render_template('contact.html', title='Contact Us', hostels=all_hostels, searchform=SearchForm())




# #################################################### UTILS


# Make a routine check where if a hostel has been deleted then all its files should also be deleted.
# Extra Routes ###





