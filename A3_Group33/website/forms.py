from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateTimeField, IntegerField, SubmitField
from wtforms.validators import InputRequired, Email, EqualTo, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed, FileRequired

ALLOWED_FILE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'}  

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[InputRequired(), Length(min=1, max=100)])
    event_date = DateTimeField('Event Date (YYYY-MM-DD HH:MM)', format='%Y-%m-%d %H:%M', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired(), Length(max=100)])
    description = TextAreaField('Description', 
            validators=[InputRequired()])
    image = FileField('Event Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE_EXTENSIONS , message='Only supports PNG, JPG, png, jpg')])    
    organizer_name = StringField('Organizer', validators=[Length(max=100)])
    submit = SubmitField('Create Event')

class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Create')

class OrderForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=1, message="Must be at least 1")])
    submit = SubmitField('Place Order')

class UploadForm(FlaskForm):
    file = FileField('Upload File', validators=[
        FileRequired('File is required'),
        FileAllowed(ALLOWED_FILE_EXTENSIONS, 'Images only!')
    ])
    submit = SubmitField('Upload')
