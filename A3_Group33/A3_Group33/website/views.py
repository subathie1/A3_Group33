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
    query = request.args.get('search', '').strip()
    if query:
        events = db.session.scalars(db.select(Event).where(Event.name.ilike(f"%{query}%"))).all()
        if not events:
            flash(f'No results found for "{query}".', 'info')
        return render_template('index.html', events=events)
    flash('Please enter a search query.', 'info')  # Added feedback for empty query
    return redirect(url_for('main.index'))  # Use the correct endpoint for redirect

# Assuming you have an events blueprint as well
event_bp = Blueprint('events', __name__)

@event_bp.route('/create', methods=['GET', 'POST'])
def create_event():
    return render_template('create_event.html')

@event_bp.route('/booking-history')
def booking_history():
    return render_template('booking_history.html')
