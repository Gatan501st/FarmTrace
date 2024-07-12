from flask import render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import current_user, login_required
import os
from werkzeug.utils import secure_filename
from app.models import Listing, Inventory, Product
from . import listings


@listings.route('/')
@login_required
def view_listings():
    products = Listing.query.all()
    my_listings = []
    inventories = current_user.inventories
    for inventory in inventories:
        for listing in inventory.listings:
            my_listings.append(listing)
    print(my_listings)
    return render_template('listings/view_listings.html', products=products, my_listings=my_listings, user=current_user)


@listings.route('/inventory', methods=['POST'])
@login_required
def create_inventory():
    inventory = Inventory(
        name=request.form.get('name'),
        description=request.form.get('description'),
        
        user_id=current_user.id,
        user=current_user
	)
    inventory.save()
    if Inventory.get('id', inventory.id) is None:
        flash('Error creating inventory', 'error')
        return redirect(url_for('listings.view_listings')), 409
    flash('Inventory created')
    return redirect(url_for('listings.view_inventory', inventory_id=inventory.id)), 201


@listings.route('/inventory/<inventory_id>')
@login_required
def view_inventory(inventory_id):
    inventory = Inventory.get('id', inventory_id)
    return render_template('listings/view_inventory.html', inventory=inventory)


@listings.route('/add', methods=['POST'])
@login_required
def add_listing():
    product = Product.get('id', request.form.get('product_id'))
    listing = Listing(
        product_name=request.form.get('name'),
        description=request.form.get('description'),
        price=request.form.get('price'),
        available_stock=request.form.get('quantity'),
        min_order=request.form.get('min_order'),
        avatar_path=request.form['avatar'],
    
        inventory_id=request.form.get('inventory_id'),
        inventory=Inventory.get('id', request.form.get('inventory_id')),
    
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
    return jsonify([{'id': product.id, 'name': product.name} for product in products])


UPLOAD_FOLDER = 'app/static/images/listings/avatars'

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
        file.save(file_path)
        return jsonify({'success': True, 'file_path': file_path})
    
    return jsonify({'success': False, 'error': 'Unknown error occurred'})

