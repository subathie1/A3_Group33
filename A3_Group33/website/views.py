from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event
from . import db
from flask_login import login_required, current_user
from .forms import EventForm


# Create the main blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    categories = Event.query.with_entities(Event.category).distinct().all()  
    events = db.session.scalars(db.select(Event)).all()

    if not events:
        flash('No events found.', 'warning')

    return render_template('index.html', events=events, categories=[cat[0] for cat in categories])

@main_bp.route('/category/<category>')
def category_view(category):
    events = Event.query.filter_by(category=category).all()
    categories = Event.query.with_entities(Event.category).distinct().all()

    if not events:
        flash(f'No events found for category: {category}', 'warning')
        return redirect(url_for('main.index'))

    return render_template('index.html', events=events, categories=[cat[0] for cat in categories])

@main_bp.route('/event/<int:id>')
def event_view(id):
    event = Event.query.get_or_404(id)  # Fetch the event by its ID
    return render_template('event.html', event=event)

@main_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('search', '').strip()

    if query:
        search_query = f"%{query}%"
        events = Event.query.filter(Event.description.like(search_query)).all()

        if not events:
            flash('No matching events found.', 'warning')
            return redirect(url_for('main.index'))

        return render_template('index.html', events=events, categories=[])

    return redirect(url_for('main.index'))

# Events Blueprint (For event management-related routes)
event_bp = Blueprint('events', __name__, url_prefix='/events')

@event_bp.route('/create', methods=['GET', 'POST'])
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        # Logic if form is valid
        return redirect(url_for('main.index'))
    else:
        print(form.errors)  # Debugging step
    return render_template('create_event.html', form=form)



@event_bp.route('/booking-history')
@login_required
def booking_history():
    return render_template('booking_history.html')

@main_bp.route('/cancel/<int:id>', methods=['GET', 'POST'])
@login_required
def cancel(id):
    event = Event.query.get(id)

    event.status = "Cancelled"
    db.session.commit()
    flash('Your event has been cancelled.')
    
    return redirect(url_for('auth.user'))
