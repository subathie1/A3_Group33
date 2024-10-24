from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
from flask_login import login_required, current_user

# Create a Blueprint for events
api_bp = Blueprint('api_events', __name__, url_prefix='/api')

@api_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        new_event = Event(
            event_name=form.event_name.data,  # Ensure this matches your model definition
            event_date=form.event_date.data,
            location=form.location.data
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('events.list_events'))  # Ensure this endpoint exists
    return render_template('create-event.html', form=form)

@api_bp.route('/<int:event_id>/comment', methods=['POST'])
@login_required
def post_comment(event_id):
    event = Event.query.get_or_404(event_id)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(
            text=form.text.data,  # Ensure this matches your model definition
            user=current_user,
            event=event
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added!', 'success')
        return redirect(url_for('events.event_details', event_id=event.id))  # Ensure this endpoint exists
    flash('Error adding comment', 'danger')  # Handle case where comment submission fails
    return redirect(url_for('events.event_details', event_id=event.id))
