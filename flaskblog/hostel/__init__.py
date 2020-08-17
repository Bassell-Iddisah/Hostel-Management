from flask import render_template, url_for, flash, redirect
from flaskblog import app, db
from flaskblog.models import Hostel
from flaskblog.forms import Hostel_Crud, SearchForm, Hostel_Update, RegisterForm, LoginForm
from flaskblog.main.util import save_image


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