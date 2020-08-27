from flask import render_template, url_for, flash, redirect, Blueprint, jsonify
from flaskblog import db
import os, shutil
from flaskblog.models import Hostel
from flaskblog.hostel.forms import Hostel_Crud, Hostel_Update
from flaskblog.main.forms import SearchForm
from flaskblog.main.util import save_image, get_name


hostel = Blueprint("hostel", __name__)


# Hostel Categories ###
@hostel.route("/luxury", methods=['GET', 'POST'])
def luxury():
    hostels = Hostel.query.filter_by(cat='luxury')
    for hostel in hostels:
        single = get_name(hostel)
    # return hostels
    return render_template('luxury.html', title='Luxury Hostels', posts=hostels, searchform=SearchForm())


@hostel.route("/comfort", methods=['GET', 'POST'])
def comfort():
    hostels = Hostel.query.filter_by(cat='comfort')
    for hostel in hostels:
        single = get_name(hostel)
    return render_template('comfort.html', title='Comfortable Hostels', posts=hostels, oiroomin=750, oiroommax=1750, searchform=SearchForm())


@hostel.route("/affordable", methods=['GET', 'POST'])
def affordable():
    hostels = Hostel.query.filter_by(cat='affordable')
    for hostel in hostels:
        single = get_name(hostel)
    # hostel_image = url_for('static', filename='/images/affordable/'+hostels.image)
    return render_template('affordable.html', title='Affordable Hostels', posts=hostels, searchform=SearchForm())


@hostel.route('/hostel_crud', methods=['GET', 'POST'])
def hostel_crud():
    form = Hostel_Crud()
    if form.validate_on_submit():
        Hostel.image = save_image(form.hostel_picture.data, form.cat.data.lower(), 'Banner', form.hostel_name.data.capitalize())
        new_hostel_name = form.hostel_name.data.replace(" ", '_')
        hostel = Hostel(name=new_hostel_name.capitalize(),
                        email=form.hostel_mail.data,
                        phone=str(form.phone_number.data),
                        price_range=form.price_range.data,
                        location=form.location.data,
                        distance=form.distance.data,
                        cat=form.cat.data.lower(),
                        image=Hostel.image)

        db.session.add(hostel)
        db.session.commit()
        flash('Hostel added successfully', 'success')
        return redirect(url_for(f"hostel.{form.cat.data.lower()}"))
    return render_template('hostel_CRUD.html', title='Alter hostel info', form=form, searchform=SearchForm())


@hostel.route('/hostel_page/<string:hostel_name>', methods=['GET', 'POST'])
def hostel_page(hostel_name):
    Query = hostel_name.capitalize()
    query_name = Query.replace(" ", "_") if " " in Query else Query
    hostel = Hostel.query.filter_by(name=query_name).first_or_404()
    return render_template('hostel_page.html', title=f'{hostel.name} Hostel',
                           current_hostel=hostel, attribs=hostel.attributes, searchform=SearchForm())


@hostel.route('/delete_hostel/<string:hostel>', methods=['GET', 'POST'])
def delete_hostel(hostel):
    hostel = Hostel.query.filter_by(name=hostel).first()
    db.session.delete(hostel)
    db.session.commit()
    flash(f"{hostel.name} Hostel successfully removed", 'success')
    return redirect(url_for('main.home'))


def delete_data(hostel):
    os.chdir(f"static/images/{hostel.cat}")
    shutil.rmtree(f"{hostel.image}")


@hostel.route('/update_hostel/<string:hostel>', methods=['GET', 'POST'])
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
        # hostel.attributes[0] = form.condition.data
        # hostel.attributes[1] = form.Intensity.data
        db.session.commit()
        flash('Hostel info update', 'success')
        return redirect(url_for('main.home'))
    return render_template('hostel_update.html', title='Update Hostel Info', current_hostel=hostel, upform=form, searchform=SearchForm())


@hostel.route('/info_posts/<string:hostel_name>', methods=['GET', 'POST'])
def info_posts(hostel_name):
    hostel = Hostel.query.filter_by(name=hostel_name).first()
    return render_template('hostel_page.html', title='Latest Hostel News', current_hostel=hostel, searchform=SearchForm())


@hostel.route('/gallery/<string:hostel_name>', methods=['GET', 'POST'])
def gallery(hostel_name):
    hostel = Hostel.query.filter_by(name=hostel_name).first()
    return render_template('gallery.html', title='Hostel Pictures', current_hostel=hostel, searchform=SearchForm())