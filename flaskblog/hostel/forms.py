from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flaskblog.models import Hostel
from wtforms import StringField, SubmitField, IntegerField, FileField
from wtforms.validators import Length, ValidationError


class Hostel_Crud(FlaskForm):
    hostel_name = StringField("Hostel Name", validators=[Length(min=2, max=20)])
    phone_number = StringField("Phone Number")
    price_range = StringField('Price Range')
    location = StringField('State location')
    distance = StringField('Distance from campus')
    cat = StringField('Hostel Category')
    hostel_mail = StringField('Hostel Email')
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
    hostel_mail = StringField('Hostel Email')
    hostel_picture = FileField('Hostel Picture', validators=[FileAllowed(['jpg', 'pgn'])])
    condition = StringField('Condition')
    Intensity = StringField('Intensity')
    submit = SubmitField("Submit")

    def validate_hostel(self, hostel_name):
        hostel = Hostel.query.filter_by(hostel_name=hostel_name.data).first()
        if hostel:
            raise ValidationError('This hostel is already in the system.')

    def validate_hostel_mail(self, hostel_mail):
        hostel = Hostel.query.filter_by(email=hostel_mail.data).first()
        if hostel:
            raise ValidationError('This hostel is already in the system.')
