from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

# Initialize extensions outside of the create_app function
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()  # Initialize Bcrypt for password hashing

# Create a function that creates a web application
def create_app():
    app = Flask(__name__)  # This is the name of the module/package that is calling this app
    app.debug = True  # Should be set to false in a production environment
    app.secret_key = 'somesecretkey'
    
    # Set the app configuration data
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'  # Adjust the path if necessary
    
    #config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 

    # Initialize extensions with the Flask app
    db.init_app(app)
    Bootstrap(app)
    login_manager.init_app(app)
    
    # Set the name of the login function that lets users log in
    login_manager.login_view = 'auth.login'

    # Create a user loader function that takes userid and returns User
    # Importing inside the create_app function avoids circular references
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, user_id)  # Use get() for primary key lookup

    # Register blueprints
    from . import views, events, auth, api
    app.register_blueprint(views.main_bp)
    app.register_blueprint(events.eventbp, url_prefix='/events')
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(api.api_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", error="Page not found"), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html', error="An unexpected error occurred on the server"), 500

    @app.context_processor
    def get_context():
        year = datetime.datetime.today().year
        return dict(year=year)

    # Create all database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app  # Move return statement to the end
