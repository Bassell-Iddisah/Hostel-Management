from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, IntegerField, FileField
from wtforms.validators import DataRequired, Length


class User_Details(FlaskForm):
    Full_Name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=30)])
    Email = StringField("E-mail", validators=[DataRequired()])
    Phone_Number = IntegerField("Phone Number", validators=[Length(min=10, max=10)])
    Article = StringField("Article")
    Submit = SubmitField("Submit")

    
class Hostel_Crud(FlaskForm):
    hostel_name = StringField("Hostel Name", validators=[Length(min=2, max=20)])
    phone_number = IntegerField("Phone Number")
    notes = StringField("Notes", validators=[Length(min=20, max=100)])
    price_range = StringField('Price Range')
    location = StringField('State location')
    distance = StringField('Distance from campus')
    cat = StringField('Hostel Category')
    hostel_picture = FileField('Hostel Picture', validators=[FileAllowed(['jpg', 'pgn'])])
    submit = SubmitField("Submit")


class Hostel_Update(FlaskForm):
    hostel_name = StringField("Hostel Name", validators=[Length(min=2, max=20)])
    phone_number = IntegerField("Phone Number")
    notes = StringField("Notes", validators=[Length(min=20, max=100)])
    price_range = StringField('Price Range')
    location = StringField('State location')
    distance = StringField('Distance from campus')
    cat = StringField('Hostel Category')
    hostel_picture = FileField('Hostel Picture', validators=[FileAllowed(['jpg', 'pgn'])])
    condition = StringField('Condition')
    Intensity = StringField('Intensity')
    advanced = SubmitField("Details")
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    search_input = StringField('Search ...', validators=[DataRequired()])
    submit = SubmitField('Search')
