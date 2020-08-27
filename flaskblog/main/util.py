import os
import os.path as path
from PIL import Image
from flask import render_template, url_for, redirect
from flaskblog import app
from flaskblog.models import Hostel
from flaskblog.main.forms import SearchForm


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
    # new_size = (350, 350)
    i = Image.open(picture)
    # i.thumbnail(new_size)
    i.save(new_path)
    return new_name


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

    return render_template('search_results.html', title=f'Search results for {query}', results=results, searchform=searchform)


def get_name(hostel):
    hostel.name = hostel.name.replace("_", " ").capitalize() if hostel else "No hostel by that name was found, please try again with the right spelling."
    print(hostel.name)
    return hostel
