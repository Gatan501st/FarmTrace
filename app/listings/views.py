from flask import render_template, request, flash, redirect, url_for, jsonify, current_app, make_response
from flask_login import current_user, login_required
import os
from werkzeug.utils import secure_filename
from app.models import Listing, Inventory, Product
from . import listings
from app.decorators import email_verified


@listings.route('/')
@login_required
def view_listings():
    products = Listing.query.all()
    my_listings = []
    if current_user.inventory:
        my_listings = current_user.inventory.listings
    return render_template('listings/view_listings.html', products=products, my_listings=my_listings, user=current_user)


@listings.route('/inventory', methods=['POST'])
@login_required
@email_verified
def create_inventory():
    inventory = Inventory(
        name=request.form.get('name') or f'{current_user.firstname}\'s Inventory',
        description=request.form.get('description') or 'A simple inventory to keep track of your listings',

        user_id=current_user.id,
        user=current_user
    )
    inventory.save()
    if Inventory.get('id', inventory.id) is None:
        flash('Error creating inventory', 'error')
        return redirect(url_for('listings.view_listings')), 409
    flash('Inventory created')
    return redirect(url_for('listings.view_inventory', inventory_id=inventory.id))


@listings.route('/inventory/<inventory_id>/edit', methods=['PUT'])
@login_required
@email_verified
def edit_inventory(inventory_id):
    inventory = Inventory.get('id', inventory_id)
    if inventory is None:
        return make_response({'message': 'Inventory not found'}), 404
    inventory.name = request.form.get('name-edited')
    inventory.description = request.form.get('description-edited')
    inventory.save()

    return make_response({'message': 'Changes saved'})


@listings.route('/inventory/<inventory_id>')
@login_required
@email_verified
def view_inventory(inventory_id):
    inventory = Inventory.get('id', inventory_id)
    return render_template('listings/view_inventory.html', inventory=inventory)


@listings.route('/add', methods=['POST'])
@login_required
@email_verified
def add_listing():
    product = Product.get('id', request.form.get('product_id'))
    listing = Listing(
        product_name=product.name,
        description=request.form.get('description'),
        price=request.form.get('price'),
        available_stock=request.form.get('quantity'),
        min_order=request.form.get('min_order'),
        avatar_path=request.form['avatar'],

        inventory_id=current_user.inventory.id,
        inventory=current_user.inventory,

        product_id=product.id,
        product=product
    )
    listing.save()
    if Listing.get('id', listing.id) is None:
        flash('Error creating listing', 'error')
        return redirect(url_for('listings.view_inventory', inventory_id=listing.inventory_id)), 409
    flash('Listing created')
    return redirect(url_for('listings.view_inventory', inventory_id=listing.inventory_id)), 201


@listings.route('/api/inventories', methods=['GET'])
@login_required
def get_inventories():
    inventories = current_user.inventories
    return jsonify([{'id': inventory.id, 'name': inventory.name} for inventory in inventories])


@listings.route('/api/products', methods=['GET'])
@login_required
def get_products():
    products = current_user.products
    return jsonify([{'id': product.id, 'name': product.name, 'description': product.description} for product in products])


UPLOAD_FOLDER = 'static/images/listings/avatars'

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@listings.route('/upload/avatar', methods=['POST'])
def upload_avatar():
    if 'avatar' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'})

    file = request.files['avatar']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'})

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(f'app/{file_path}')
        return jsonify({'success': True, 'file_path': file_path})

    return jsonify({'success': False, 'error': 'Unknown error occurred'})
