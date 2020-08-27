from flask import render_template, url_for, flash, redirect, Blueprint
from flaskblog import app, db, bcrypt
from flaskblog.models import User
from flaskblog.main.forms import SearchForm
from flaskblog.user.forms import RegisterForm, LoginForm
from flask_login import current_user, login_user, logout_user


user = Blueprint("user", __name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    logform = LoginForm()
    if logform.validate_on_submit():
        email = logform.email.data
        student = User.query.filter_by(email=email).first()
        if student and bcrypt.check_password_hash(student.password, logform.password.data):
            login_user(student)
            flash(f'{current_user.username} login successful', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Either email or password incorrect, please check and try again', 'warning')
    return render_template('login.html', form=logform, searchform=SearchForm())


@app.route('/sign_out')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


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
        return redirect(url_for('main.home'))
    return render_template('register.html', legend='Register', form=form, searchform=SearchForm())


@app.route('/update account info', methods=['GET', 'POST'])
def account():
    return 'Account'
