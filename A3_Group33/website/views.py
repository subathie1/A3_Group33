from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event
from . import db

# Create the main blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    if not events:
        flash('No events found.', 'warning')
    return render_template('index.html', events=events)

@main_bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        destinations = db.session.scalars(db.select(Event)).where(Event.description.like(query))
        return render_template('index.html', destinations=destinations)
    else:
        return redirect(url_for('main.index'))

# Assuming you have an events blueprint as well
event_bp = Blueprint('events', __name__)

@event_bp.route('/create', methods=['GET', 'POST'])
def create_event():
    return render_template('create_event.html')

@event_bp.route('/booking-history')
def booking_history():
    return render_template('booking_history.html')
