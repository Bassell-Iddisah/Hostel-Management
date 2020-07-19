import os
import os.path as path
from PIL import Image
from flask import render_template, url_for, flash, redirect
from flaskblog import app, db
from flaskblog.models import Hostel, Hostel_Attributes
from flaskblog.forms import Hostel_Crud, SearchForm, Hostel_Update
from flask_login import current_user
import secrets


# Core Routes ###
@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.search_input.data
        results = Hostel.query.filter_by(name=query)
    image = url_for('static', filename='images/'+'Gaza.jpg')
    return render_template("home.html", title='Home', posts=Hostel.query.all(),
                           about='jaghgisga', image=image, form=form)


@app.route("/about")
def about():
    return render_template('about.html', title='About Us')


@app.route("/contact")
def contact():
    return render_template('contact.html', title='Contact Us')


# Hostel Categories ###
@app.route("/luxury")
def luxury():
    hostels = Hostel.query.filter_by(cat='luxury')
    return render_template('luxury.html', title='Luxury Hostels', posts=hostels)


@app.route("/comfort")
def comfort():
    hostels = Hostel.query.filter_by(cat='comfort')
    return render_template('comfort.html', title='Comfortable Hostels', posts=hostels, oiroomin=750, oiroommax=1750)


@app.route("/affordable")
def affordable():
    hostels = Hostel.query.filter_by(cat='affordable')
    return render_template('affordable.html', title='Affordable Hostels', posts=hostels)


# Get and save images submitted by forms
def save_image(picture, cat=None, name=None, Hostel=None):
    # Set new picture path and new image size
    __, ext = path.splitext(picture.filename)
    new_name = f"{Hostel}_{name}{ext}"
    new_name = new_name.replace(" ", "_")
    if path.exists(f'{app.root_path}/static/images/{cat}/'):
        new_path = path.join(app.root_path, f'static/images/{cat}/{new_name}')
    else:
        os.makedirs(f'{app.root_path}/static/images/{cat}/')
        new_path = path.join(app.root_path, f'static/images/{cat}/{new_name}')


    new_size = (350, 350)

    i = Image.open(picture)
    i.thumbnail(new_size)
    i.save(new_path)
    return new_name


# Make a routine check where if a hostel has been deleted then all its files should also be deleted.
# Extra Routes ###
@app.route('/hostel_crud', methods=['GET', 'POST'])
def hostel_crud():
    form = Hostel_Crud()
    if form.validate_on_submit():
        Hostel.image = save_image(form.hostel_picture.data, form.cat.data.lower(), 'Banner', form.hostel_name.data)

        new_hostel_name = form.hostel_name.data.replace(" ", '_')
        print(new_hostel_name)

        hostel = Hostel(name=new_hostel_name,
                        phone=form.phone_number.data,
                        price_range=form.price_range.data,
                        location=form.location.data,
                        distance=form.distance.data,
                        cat=form.cat.data.lower(),
                        image=Hostel.image)

        db.session.add(hostel)
        db.session.commit()
        flash('Hostel added successfully', 'success')
        return redirect(url_for(form.cat.data))
    return render_template('hostel_CRUD.html', title='Alter hostel info', form=form)


@app.route('/hostel_page/<string:hostel_name>')
def hostel_page(hostel_name):
    counter = 0
    hostel = Hostel.query.filter_by(name=hostel_name).first()
    # Trying to test if i.Intensity is an integer
    for i in hostel.attributes:
        if i.Intensity is int:
            print(i.Intensity)
    return render_template('hostel_page.html', title=f'{hostel.name} Hostel',
                           current_hostel=hostel, attribs=hostel.attributes)


@app.route('/delete_hostel/<string:hostel>')
def delete_hostel(hostel):
    # Put a flask alert that confirms if user wants to delete the hostel
    print(hostel)
    # db.session.delete(hostel)
    # db.session.commit()
    # flash("hostel successfully removed", 'success')
    return redirect(url_for('home'))


@app.route('/update_hostel/<string:hostel>', methods=['GET', 'POST'])
def update_hostel(hostel):
    form = Hostel_Update()
    hostel = Hostel.query.filter_by(name=hostel).first()
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
    return render_template('hostel_update.html', title='Update Hostel Info', current_hostel=hostel, upform=form)


@app.route('/info_posts/<string:hostel_name>')
def info_posts(hostel_name):
    hostel = Hostel.query.filter_by(name=hostel_name).first()
    return render_template('hostel_page.html', title='Latest Hostel News', current_hostel=hostel)


@app.route('/gallery/<string:hostel_name>', methods=['GET', 'POST'])
def gallery(hostel_name):
    hostel = Hostel.query.filter_by(name=hostel_name).first()
    return render_template('gallery.html', title='Hostel Pictures', current_hostel=hostel)


@app.route('/search_results/')
def search_results():
    form = SearchForm()
    query = form.query.data()
    return render_template('search_results.html', title=f'Search results for {query}')
