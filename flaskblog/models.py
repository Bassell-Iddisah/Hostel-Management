from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    image_file = db.Column(db.String, default='default.jpg', nullable=False)
    is_admin = db.Column(db.Integer, default=0, nullable=False)
    #posts = db.relationship('Posts', backref='author', lazy=True)

    def __repr__(self):
        return f"User( 'username:{ self.username }', 'id:{ self.id }','image:{ self.image_file }')"


# Main hostel table will contain basic hostel info
class Hostel(db.Model):
    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.Integer(), nullable=False)
    cat = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    image = db.Column(db.String(60), nullable=False, default='def_hostel_image.jpg')
    price_range = db.Column(db.Integer(), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    distance = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer(), default=None)
    attributes = db.relationship('Hostel_Attributes', backref='which_hostel', lazy=True)

    def __repr__(self):
        return f"Hostel( 'name:{ self.name }', 'id:{ self.id }','phone:{ self.phone }','image:{ self.image }')"


# Hostel _attributes table will contain deep and extensive hostel info
class Hostel_Attributes(db.Model):
    id = db.Column(db.Integer(), unique=True, nullable=False, primary_key=True)
    condition = db.Column(db.String(20), nullable=False)
    Intensity = db.Column(db.String(20), nullable=False)
    belongs_to = db.Column(db.Integer, db.ForeignKey('hostel.id'), nullable=False)

    def __repr__(self):
        return f"Hostel_Attributes( '{ self.id }', 'Condition:{ self.condition }','Intensity:{ self.Intensity }')"


class Hostel_Images(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    img_name = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=False)
    belongs_to = db.Column(db.Integer, db.ForeignKey('hostel.id'), nullable=False)

    def __repr__(self):
        return f"Hostel_Images('Image:{self.image_name}', Belongs to: '{self.belongs_to}')"
