import os
import os.path as path
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.models import Hostel, Hostel_Attributes, User
from flaskblog.forms import Hostel_Crud, SearchForm, Hostel_Update, RegisterForm, LoginForm
from flask_login import current_user, login_required, login_user, logout_user


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


@app.route('/search_results/<string:query>', methods=['GET', 'POST'])
def search_results(query):
    searchform = SearchForm()
    # Have a 404 page saying that Hostel not found
    if searchform.validate_on_submit():
        query = searchform.search_input.data
        return redirect(url_for('search_results', query=query))
    Query = query.capitalize()
    query_name = Query.replace(" ", "_") if " " in Query else Query
    results = Hostel.query.filter_by(name=query_name).first_or_404()

    results.name = results.name.replace("_", " ") if results else "No Hostel was found with that name."
    # print(query)
    # new_query = query.replace(" ", "_").capitalize() if " " in query else None
    # print(new_query)
    # results = Hostel.query.filter_by(name=new_query).first_or_404()
    # print(results)
    # results.name = results.name.replace("_", " ").capitalize() if results else None
    # print(results.name)
    # # return str(results)
    # # results.name.replace("_", " ") if "_" in results else None
    return render_template('search_results.html', title=f'Search results for {query}', results=results, searchform=searchform)
    #404 Hostel not found
