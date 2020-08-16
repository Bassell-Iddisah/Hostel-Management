import os
import os.path as path
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.models import Hostel, Hostel_Attributes, User
from flaskblog.forms import Hostel_Crud, SearchForm, Hostel_Update, RegisterForm, LoginForm
from flask_login import current_user, login_required, login_user, logout_user


# Core Routes ###
@app.route("/", methods=['GET', 'POST'])
@login_required
def home():
    searchform = SearchForm()
    all_hostels = Hostel.query.all()
    if searchform.validate_on_submit():
        query = searchform.search_input.data
        return redirect(url_for('search_results', query=query))
    return render_template("home.html", title='Home', searchform=SearchForm(), current_user=current_user, hostels=all_hostels)

@app.route('/login', methods=['GET', 'POST'])
def login():
    logform = LoginForm()
    if logform.validate_on_submit():
        email = logform.email.data
        student = User.query.filter_by(email=email).first()
        if student and bcrypt.check_password_hash(student.password, logform.password.data):
            login_user(student)
            flash(f'{current_user.username} login successful', 'success')
            return redirect(url_for('home'))
    return render_template('login.html', form=logform, searchform=SearchForm())


@app.route('/sign_out')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.fullname.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.confirmpassword.data)
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {username}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', legend='Register', form=form, searchform=SearchForm())


@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', title='About Us', searchform=SearchForm())


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    all_hostels = Hostel.query.all()
    return render_template('contact.html', title='Contact Us', hostels=all_hostels, searchform=SearchForm())


# Hostel Categories ###
@app.route("/luxury", methods=['GET', 'POST'])
def luxury():
    hostels = Hostel.query.filter_by(cat='luxury')
    return render_template('luxury.html', title='Luxury Hostels', posts=hostels, searchform=SearchForm())


@app.route("/comfort", methods=['GET', 'POST'])
def comfort():
    hostels = Hostel.query.filter_by(cat='comfort')
    return render_template('comfort.html', title='Comfortable Hostels', posts=hostels, oiroomin=750, oiroommax=1750, searchform=SearchForm())


@app.route("/affordable", methods=['GET', 'POST'])
def affordable():
    hostels = Hostel.query.filter_by(cat='affordable')
    return render_template('affordable.html', title='Affordable Hostels', posts=hostels, searchform=SearchForm())


# Get and save images submitted by forms
def save_image(picture, cat=None, name=None, Hostel=None):
    # Set new picture path and new image size
    __, ext = path.splitext(picture.filename)
    new_name = f"{Hostel}_{name}{ext}"
    new_name = new_name.replace(" ", "_")
    # Test if path exists else create path
    if path.exists(f'{app.root_path}/static/images/{cat}/'):
        new_path = path.join(app.root_path, f'static/images/{cat}/{new_name}')
    else:
        os.makedirs(f'{app.root_path}/static/images/{cat}/')
        new_path = path.join(app.root_path, f'static/images/{cat}/{new_name}')
    # Apply new size and save image
    new_size = (350, 350)
    i = Image.open(picture)
    i.thumbnail(new_size)
    i.save(new_path)
    return new_name


# Get Hostel name and take out all underscores
def get_no_underscore(hostel):
    # Test for hostel existance and replace all underscores with spaces then return new hostel name
    hostel.name = hostel.name.replace("_", " ") if "_" in hostel.name else None if hostel else print()
    return hostel.name


# Make a routine check where if a hostel has been deleted then all its files should also be deleted.
# Extra Routes ###
@app.route('/hostel_crud', methods=['GET', 'POST'])
def hostel_crud():
    form = Hostel_Crud()
    if form.validate_on_submit():
        Hostel.image = save_image(form.hostel_picture.data, form.cat.data.lower(), 'Banner', form.hostel_name.data.capitalize())
        new_hostel_name = form.hostel_name.data.replace(" ", '_')
        hostel = Hostel(name=new_hostel_name.capitalize(),
                        phone=str(form.phone_number.data),
                        price_range=form.price_range.data,
                        location=form.location.data,
                        distance=form.distance.data,
                        cat=form.cat.data.lower(),
                        image=Hostel.image)

        db.session.add(hostel)
        db.session.commit()
        flash('Hostel added successfully', 'success')
        return redirect(url_for(form.cat.data.lower()))
    return render_template('hostel_CRUD.html', title='Alter hostel info', form=form, searchform=SearchForm())


@app.route('/search_results/<string:query>', methods=['GET', 'POST'])
def search_results(query):
    searchform = SearchForm()
    # Have a 404 page saying that Hostel not found
    if searchform.validate_on_submit():
        query = searchform.search_input.data
        return redirect(url_for('search_results', query=query))
    print(query)
    new_query = query.replace(" ", "_").capitalize() if " " in query else None
    print(new_query)
    results = Hostel.query.filter_by(name=new_query).first_or_404()cl
    print(results)
    results.name = results.name.replace("_", " ").capitalize() if results else None
    print(results.name)
    # return str(results)
    # results.name.replace("_", " ") if "_" in results else None
    return render_template('home.html', title=f'Search results for {query}', results=results, searchform=searchform)
    #404 Hostel not found


@app.route('/hostel_page/<string:hostel_name>', methods=['GET', 'POST'])
def hostel_page(hostel_name):
    counter = 0
    hostel = Hostel.query.filter_by(name=hostel_name).first()
    # Trying to test if i.Intensity is an integer
    for i in hostel.attributes:
        if i.Intensity is int:
            print(i.Intensity)
    return render_template('hostel_page.html', title=f'{hostel.name} Hostel',
                           current_hostel=hostel, attribs=hostel.attributes, searchform=SearchForm())


@app.route('/delete_hostel/<string:hostel>', methods=['GET', 'POST'])
def delete_hostel(hostel):
    hostel = Hostel.query.filter_by(name=hostel).first()
    db.session.delete(hostel)
    db.session.commit()
    flash(f"{hostel.name} Hostel successfully removed", 'success')
    return redirect(url_for('home'))


@app.route('/update_hostel/<string:hostel>', methods=['GET', 'POST'])
def update_hostel(hostel):
    form = Hostel_Update()
    hostel = Hostel.query.filter_by(name=hostel).first()
    form.hostel_name.data = hostel.name
    form.phone_number.data = hostel.phone
    form.cat.data = hostel.cat
    form.price_range.data = hostel.price_range
    form.location.data = hostel.location
    form.distance.data = hostel.distance
    # form.condition.data = hostel.attributes[0]
    # form.Intensity.data = hostel.attributes[1]
    if form.validate_on_submit():
        hostel.name = form.hostel_name.data
        hostel.phone = form.phone_number.data
        hostel.cat = form.cat.data.lower()
        hostel.image = save_image(form.hostel_picture.data, hostel.cat, "Banner", hostel.name )
        hostel.price_range = form.price_range.data
        hostel.location = form.location.data
        hostel.distance = form.distance.data
        hostel.attributes[0] = form.condition.data
        hostel.attributes[1] = form.Intensity.data
        db.session.commit()
        flash('Hostel info update', 'success')
        return redirect('home')
    return render_template('hostel_update.html', title='Update Hostel Info', current_hostel=hostel, upform=form, searchform=SearchForm())


@app.route('/info_posts/<string:hostel_name>', methods=['GET', 'POST'])
def info_posts(hostel_name):
    hostel = Hostel.query.filter_by(name=hostel_name).first()
    return render_template('hostel_page.html', title='Latest Hostel News', current_hostel=hostel, searchform=SearchForm())


@app.route('/gallery/<string:hostel_name>', methods=['GET', 'POST'])
def gallery(hostel_name):
    hostel = Hostel.query.filter_by(name=hostel_name).first()
    return render_template('gallery.html', title='Hostel Pictures', current_hostel=hostel, searchform=SearchForm())
