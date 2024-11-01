from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime

# Initialize extensions outside of the create_app function
db = SQLAlchemy()  # Initialize db here to avoid circular imports
login_manager = LoginManager()
bcrypt = Bcrypt()  # Initialize Bcrypt for password hashing

def create_app():
    app = Flask(__name__)
    app.debug = True  # Should be set to False in a production environment
    app.secret_key = 'somesecretkey'
    
    # Set the app configuration data
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    app.config['UPLOAD_FOLDER'] = '/static/image'

    # Initialize extensions with the Flask app
    db.init_app(app)
    Bootstrap(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Import User and Event models here to avoid circular import issues
    with app.app_context():
        from .models import User, Event

        @login_manager.user_loader
        def load_user(user_id):
            return db.session.get(User, user_id)

        # Register blueprints
        from . import views, events, auth, api
        app.register_blueprint(views.main_bp)
        app.register_blueprint(events.eventbp, url_prefix='/events')
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(api.api_bp)

        # Error handlers
        @app.errorhandler(404)
        def not_found(e):
            return render_template("404.html", error="Page not found"), 404

        @app.errorhandler(500)
        def internal_server_error(e):
            return render_template('500.html', error="An unexpected error occurred on the server"), 500

        # Context processor to add the current year
        @app.context_processor
        def get_context():
            year = datetime.datetime.today().year
            return dict(year=year)

        # Create all database tables if they don't exist
        db.create_all()

        # Add dummy data if no events exist
        if not Event.query.first():
            default_user = User.query.first() or User(
                name="DefaultUser", emailid="default@example.com",
                password_hash="dummyhash", street_name="123 Default St",
                contact_number="1234567890"
            )
            db.session.add(default_user)
            db.session.commit()

            dummy_event = Event(
                name="Sample Music Festival",
                description="A vibrant music festival featuring top artists.",
                event_date=datetime.datetime(2024, 12, 31, 18, 0),
                location="Sample Venue",
                price=50.00,
                ticketsAvailable=100,
                status="Open",
                category="Festival",
                user_id=default_user.id,
                image="/static/image/sample_event.jpg"
            )
            db.session.add(dummy_event)
            db.session.commit()

    return app
