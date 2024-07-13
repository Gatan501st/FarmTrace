from flask import render_template, redirect, url_for, request, make_response
from flask_login import current_user, login_required
from . import orders
from app.models import Listing, Order, Product
from datetime import datetime


def calculate_tracking_progress(checkpoints):
    total_checkpoints = len(checkpoints)
    completed_checkpoints = len(
        [checkpoint for checkpoint in checkpoints if checkpoint.get('status')])
    return (completed_checkpoints / total_checkpoints) * 100 if total_checkpoints else 0


@orders.route('/<order_id>', methods=['GET'])
@login_required
def view_order(order_id):
    order = Order.query.get_or_404(order_id)
    checkpoints = None
    tracking_progress = 0
    if order.shipment:
        checkpoints = order.shipment.get_checkpoints
        tracking_progress = calculate_tracking_progress(checkpoints)
    return render_template('orders/view_order.html', order=order, tracking_progress=tracking_progress)


@orders.route('/place_order/<listing_id>', methods=['GET', 'POST'])
def place_order(listing_id):
    listing = Listing.get('id', listing_id)
    product = Product.get('id', listing.product_id)
    if request.method == 'POST':
        order = Order(
            quantity=request.form.get('quantity'),
            total_price=listing.price * int(request.form.get('quantity')),
            order_date=datetime.now(),

            payment_method=request.form.get('payment_method'),

            delivery_address=request.form.get('delivery_address'),

            product_id=product.id,

            listing_id=listing.id,

            recipient_id=current_user.id,
            sender_id=listing.inventory.user_id
        )
        order.save()
    return render_template('orders/place_order.html', listing=listing)


@orders.route('/cart')
def cart_view():
    total = sum(item['product']['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)


@orders.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form['quantity'])
    for item in cart:
        if item['product']['id'] == product_id:
            item['quantity'] = quantity
            break
    return redirect(url_for('orders.cart_view'))


@orders.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    global cart
    cart = [item for item in cart if item['product']['id'] != product_id]
    return redirect(url_for('orders.cart_view'))
