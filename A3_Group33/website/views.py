from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .models import Event, Order
from . import db
from flask_login import login_required, current_user
from .forms import EventForm, OrderForm
from datetime import datetime

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

@event_bp.route('/<int:event_id>/order', methods=['GET', 'POST'])
@login_required
def create_order(event_id):
    event = Event.query.get_or_404(event_id)
    form = OrderForm()

    if event.status != 'Open':
        flash('This event is not available for booking.', 'danger')
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        if not form.ticket_type.data:
           flash('Ticket type is required.', 'danger')
           return redirect(url_for('events.create_order', event_id=event.id))

        print(f"Ticket Type: {form.ticket_type.data}") 
        print(f"Quantity: {form.quantity.data}")

        quantity = form.quantity.data
        ticket_type = form.ticket_type.data

        if quantity > event.tickets_available:
            flash('Not enough tickets available.', 'danger')
            return redirect(url_for('event_bp.event_view', id=event.id))

        # Create a new booking
        new_order = Order(
            quantity=quantity,
            order_date=datetime.now(),
            status='pending',
            ticket_type=ticket_type,
            event_id=event.id,
            user_id=current_user.id
        )

        event.ticketsAvailable -= form.quantity.data  # Reduce ticket count

       # Save the new order
        try:
          db.session.add(new_order)
          db.session.commit()
          flash('Order placed successfully!', 'success')
        except Exception as e:
          db.session.rollback()
          flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for('event_bp.booking_confirmation', order_id=new_order.id))

    return render_template('create_order.html', form=form, event=event)




@main_bp.route('/booking-history')
@login_required
def booking_history():
    orders = Order.query.filter_by(user_id=current_user.id).all()

    if not orders:
        flash('No bookings found.', 'warning')
        return redirect(url_for('main.index'))

    return render_template('booking_history.html', orders=orders)


@event_bp.route('/booking/<int:order_id>/confirmation')
@login_required
def booking_confirmation(order_id):
    order = db.session.get(Order, order_id)

    if order is None or order.user_id != current_user.id:
        flash('Invalid order ID.', 'danger')
        return redirect(url_for('main.index'))

    return render_template('booking_confirmation.html', order=order)


@main_bp.route('/cancel/<int:id>', methods=['GET', 'POST'])
@login_required
def cancel(id):
    event = Event.query.get(id)

    event.status = "Cancelled"
    db.session.commit()
    flash('Your event has been cancelled.')
    
    return redirect(url_for('auth.user'))
