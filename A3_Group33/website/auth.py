from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db

# Create a blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # Validate the form on POST request
    if form.validate_on_submit():
        # Get username, password, and email from the form
        uname = form.user_name.data
        pwd = form.password.data
        email = form.email_id.data
        street = form.street_name.data
        contact = form.contact_number.data
        
        # Check if a user exists
        user = db.session.scalar(db.select(User).where(User.name == uname))
        if user:  # This returns true when user is not None
            flash('Username already exists, please try another', 'danger')
            return redirect(url_for('auth.register'))
        
        # Don't store the password in plaintext
        pwd_hash = generate_password_hash(pwd)
        
        # Create a new User model object
        new_user = User(name=uname, password_hash=pwd_hash, emailid=email, street_name=street,
            contact_number=contact)
        db.session.add(new_user)
        db.session.commit()  # Commit to the database
        
        flash('Account created successfully!', 'success')  # Success message
        return redirect(url_for('main.index'))
    
    # Render the registration form on GET request
    return render_template('user.html', form=form, heading='Register')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # Get the username and password from the form
        user_name = login_form.user_name.data
        password = login_form.password.data
        
        # Retrieve user from the database
        user = db.session.scalar(db.select(User).where(User.name == user_name))
        
        # Check for user existence and password correctness
        if user is None or not check_password_hash(user.password_hash, password):
            flash('Invalid username or password', 'danger')
        else:
            # All good, set the login_user of Flask-Login to manage the user
            login_user(user)
            flash('Login successful!', 'success')  # Success message
            return redirect(url_for('main.index'))

    return render_template('user.html', form=login_form, heading='Login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')  # Inform user about logout
    return redirect(url_for('main.index'))
