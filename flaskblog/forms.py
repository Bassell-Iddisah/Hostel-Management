from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flaskblog.models import User, Hostel
from wtforms import StringField, SubmitField, IntegerField, FileField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegisterForm(FlaskForm):
    fullname = StringField("Full Name", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField('Choose Password', validators=[DataRequired()])
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Submit")

    def validate_username(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email alreade exists, please choose a new one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')

    
class Hostel_Crud(FlaskForm):
    hostel_name = StringField("Hostel Name", validators=[Length(min=2, max=20)])
    phone_number = StringField("Phone Number")
    price_range = StringField('Price Range')
    location = StringField('State location')
    distance = StringField('Distance from campus')
    cat = StringField('Hostel Category')
    hostel_picture = FileField('Hostel Picture', validators=[FileAllowed(['jpg', 'pgn'])])
    submit = SubmitField("Submit")

    def validate_hostel(self, hostel_name):
        hostel = Hostel.query.filter_by(hostel_name=hostel_name.data).first()
        if hostel:
            raise ValidationError('This hostel is already in the system.')


class Hostel_Update(FlaskForm):
    hostel_name = StringField("Hostel Name", validators=[Length(min=2, max=20)])
    phone_number = IntegerField("Phone Number")
    price_range = StringField('Price Range')
    location = StringField('State location')
    distance = StringField('Distance from campus')
    cat = StringField('Hostel Category')
    hostel_picture = FileField('Hostel Picture', validators=[FileAllowed(['jpg', 'pgn'])])
    condition = StringField('Condition')
    Intensity = StringField('Intensity')
    submit = SubmitField("Submit")

    def validate_hostel(self, hostel_name):
        hostel = Hostel.query.filter_by(hostel_name=hostel_name.data).first()
        if hostel:
            raise ValidationError('This hostel is already in the system.')


class SearchForm(FlaskForm):
    search_input = StringField('Search ...', validators=[DataRequired()])
    submit = SubmitField('Search')


class images(FlaskForm):
    Numberoffields = StringField("", validators=[DataRequired()])
