from flask import Blueprint, render_template, redirect, url_for, flash
from .models import Event, Comment, Order
from .forms import EventForm, CommentForm, OrderForm
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
    orderForm = OrderForm()
    return render_template('events/show.html', event=event, form=form, orderForm=orderForm)

@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            name=form.name.data,
            description=form.description.data,
            event_date=form.event_date.data,
            category=form.category.data,  # Ensure this value is populated
            location=form.location.data,
            user_id=current_user.id,
            image=check_upload_file(form),
            status=form.status.data,
            ticketsAvailable=form.tickets_available.data,
            price=form.price.data  # Set price from form data
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('events.show', event_id=event.id))

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
            text=form.text.data,
            user_id=current_user.id, 
            event_id=event.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted!', 'success')
    return redirect(url_for('events.show', event_id=event.id))  # Redirect to the event show route

@eventbp.route('/<int:event_id>/order', methods=['POST'])
@login_required
def create_order(event_id):
    form = OrderForm()
    event = Event.query.get_or_404(event_id)
    if form.validate_on_submit():
        order = Order(
            quantity=form.quantity.data,
            ticket_type=form.ticket_type.data,
            user_id=current_user.id, 
            event_id=event.id,
            price=event.price  # Use event's price for the order
        )
        event.ticketsAvailable -= form.quantity.data  # Reduce available tickets

        try:
            db.session.add(order)
            db.session.commit()
            flash('Order placed successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('events.booking_history'))  # Redirect to booking history

@eventbp.route('/history')
@login_required
def booking_history():
    orders = Order.query.filter_by(user_id=current_user.id).all()

    # Debugging: Print the order details to verify
    for order in orders:
        print(f"Order ID: {order.id}, Event: {order.event.name}, Quantity: {order.quantity}")

    if not orders:
        flash('No bookings found.', 'warning')
        return redirect(url_for('main.index'))

    return render_template('booking_history.html', orders=orders)

@eventbp.route('/save', methods=['POST'])
@login_required
def save_event():
    # Logic to save the event data from the form (implement as needed)
    flash('Event saved successfully!', 'success')
    return redirect(url_for('events.create_event'))  # Redirect back to the create event page or the event list
