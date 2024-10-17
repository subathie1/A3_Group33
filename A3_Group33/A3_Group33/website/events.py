from flask import Blueprint, render_template, redirect, url_for, flash
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
from flask_login import login_required, current_user

# Create a blueprint for events
eventbp = Blueprint('events', __name__, url_prefix='/events')

@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            event_name=form.name.data,  # Ensure this matches your model's field name
            event_date=form.event_date.data,
            location=form.location.data,
            description=form.description.data,
            organizer_name=current_user.name  # Use current_user to set the organizer
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('events.list_events'))  # Ensure this route exists
    return render_template('create_event.html', form=form)

@eventbp.route('/<int:event_id>/comment', methods=['POST'])
@login_required
def post_comment(event_id):
    form = CommentForm()
    event = Event.query.get_or_404(event_id)
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data, 
            user=current_user, 
            event=event
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted!', 'success')
    return redirect(url_for('events.event_details', event_id=event.id))  # Fixed redirect to use the correct parameter

@eventbp.route('/history')
@login_required
def booking_history():
    return render_template('booking_history.html')

@eventbp.route('/save', methods=['POST'])
@login_required
def save_event():
    # Logic to save the event data from the form
    flash('Event saved successfully!', 'success')
    return redirect(url_for('events.create_event'))  # Redirect back to the create event page or the event list
