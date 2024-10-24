from flask import Blueprint, render_template, redirect, url_for, flash
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename

eventbp = Blueprint('events', __name__, url_prefix='/events')

@eventbp.route('/<int:event_id>')
def show(event_id):
    # Retrieve the event using the event_id
    event = db.session.scalar(db.select(Event).where(Event.id == event_id))
    form = CommentForm()  # Create the comment form
    return render_template('events/show.html', event=event, form=form)

@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        print("Form data is valid.")  # Debugging line
        db_upload_path = check_upload_file(form)
        print(f"Image path: {db_upload_path}") 

        event = Event(
            name=form.name.data,
            event_date=form.event_date.data,
            location=form.location.data,
            description=form.description.data,
            user_id=current_user.id,  # Ensure this references the current user
            image =db_upload_path  # Use the path returned from check_upload_file
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('events.show', event_id=event.id))
    
    print("Form data is not valid.")  # Debugging line
    return render_template('create_event_wtforms.html', form=form)


def check_upload_file(form):
    # Get file data from form
    fp = form.image.data  # Ensure this matches the name in your form
    filename = fp.filename
    # Get the current path of the module file and store image file relative to this path  
    BASE_PATH = os.path.dirname(__file__)
    # Upload file location – directory of this file/static/image
    upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
    # Store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/image/' + secure_filename(filename)
    # Save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path


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
    return redirect(url_for('booking_history.html', event_id=event.id))  # Redirect to the event show route




@eventbp.route('/history')
@login_required
def booking_history():
    return render_template('booking_history.html')

@eventbp.route('/save', methods=['POST'])
@login_required
def save_event():
    # Logic to save the event data from the form (implement as needed)
    flash('Event saved successfully!', 'success')
    return redirect(url_for('events.create_event'))  # Redirect back to the create event page or the event list
