import json
from datetime import datetime
from app.models import Shipment, Order
from flask import make_response, redirect, url_for, flash, abort, render_template, request
from flask_login import current_user
from app.utils import generate_qr


from . import shipments


@shipments.route('/create', methods=['POST'])
def create_shipment():
    shipment = Shipment(
        destination=request.form.get('destination'),
        checkpoints=json.dumps({
            'locatiion': 'Main WareHouse',
            'date': f'{datetime.now()}',
            'status': 'Processing'
        }),
        user_id=current_user.id
    )
    shipment.save()
    if Shipment.get('id', shipment.id) is None:
        return make_response({"message": 'Error creating shipment'})
    return redirect(url_for('shipments.view_shipment', shipment_id=shipment.id))


@shipments.route('/<shipment_id>')
def view_shipment(shipment_id):
    shipment = Shipment.get('id', shipment_id)
    if not shipment:
        flash('Shipment not found')
        return redirect(url_for('accounts.dashboard'))
    if shipment.user_id != current_user.id:
        abort(403)
    return render_template('shipments/view_shipment.html', shipment=shipment)


@shipments.route('<shipment_id>/add_order/<order_id>')
def add_shipment_order(shipment_id, order_id):
    shipment = Shipment.get('id', shipment_id)
    if not shipment:
        return make_response({'message': 'Shipment not found'})
    order = Order.get('id', order_id)
    if not order:
        return make_response({'message': 'Order not found'})
    order.shipment_id = shipment.id
    order.qrcode = generate_qr(order, f'{order.id}.jpg')
    order.save()
    return make_response({'message': 'Order added successfully'})


@shipments.route('<shipment_id>/dispatch')
def dispatch_shipment(shipment_id):
    shipment = Shipment.get('id', shipment_id)
    if shipment is None:
        flash('Shipment not found')
        return redirect(url_for('accounts.dashboard'))
    shipment.status = 'Dispatched'
    shipment.save()
    flash('Shipment dispatched for shipping')
    return redirect(url_for('accounts.dashboard'))