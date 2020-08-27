from flask import render_template, url_for, redirect, Blueprint
from flaskblog.models import Hostel
from flaskblog.main.forms import SearchForm
from flask_login import current_user, login_required
from flaskblog.main.util import get_name


main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@login_required
def home():
    searchform = SearchForm()
    all_hostels = Hostel.query.all()
    if searchform.validate_on_submit():
        query = searchform.search_input.data
        return redirect(url_for('search_results', query=query))
    for hostels in all_hostels:
        single = get_name(hostels)
    return render_template("home.html", title='Home', searchform=SearchForm(),
                           current_user=current_user, hostels=all_hostels
                           , l_about='Description', c_about='Description', a_about='Description')


@main.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About Us', searchform=SearchForm())


@main.route("/contact", methods=['GET', 'POST'])
def contact():
    all_hostels = Hostel.query.all()
    for hostels in all_hostels:
        single = get_name(hostels)
    return render_template('contact.html', title='Contact Us', hostels=all_hostels, searchform=SearchForm())
