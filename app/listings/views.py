from flask import render_template, make_response, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_required

from app.models import Listing, Inventory, Product
from . import listings

@listings.route('/')
@login_required
def view_listings():
    products = [
        {
            'name': 'Granular Fertilizer',
            'description': 'Premium quality granular fertilizer for healthy plants. Organic and eco-friendly. 100% natural. No chemicals.',
            'price': 2.99,
            'batches': [{'size': 24}, {'size': 48}, {'size': 96}],
            'image_url': 'https://www.fertilizer-machine.net/wp-content/uploads/2018/06/types-of-fertilizer.jpg'
        },
        {
            'name': 'Nitrogen Fertilizer hi-res',
            'description': 'High-quality nitrogen fertilizer for healthy plants. 100% organic and eco-friendly. 20% Nitrogen. 80% natural minerals. 0% chemicals.',
            'price': 1.49,
            'batches': [{'size': 10}, {'size': 20}, {'size': 50}],
            'image_url': 'https://c8.alamy.com/comp/2R1HDEP/pile-of-inorganic-fertilizer-aka-synthetic-or-chemical-fertilizer-minerals-like-nitrogen-phosphorus-and-potassium-needs-for-different-plants-2R1HDEP.jpg'
        },
        {
            'name': 'NPK 20 20 20',
            'description': 'Balanced NPK fertilizer for all types of plants. 20% Nitrogen, 20% Phosphorus, 20% Potassium. 100% organic.',
            'price': 3.99,
            'batches': [{'size': 12}, {'size': 24}, {'size': 48}],
            'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1Kix8lqdHDBXNoFEg8_GI7JRdk5E1Nx9v7w&s'
        },
        {
            'name': 'Amino Acid Granular - China',
            'description': 'Amino acid granular fertilizer for healthy plants. 100% organic and eco-friendly. 20% amino acid. 80% natural minerals.',
            'price': 2.49,
            'batches': [{'size': 20}, {'size': 40}, {'size': 80}],
            'image_url': 'https://image.made-in-china.com/44f3j00NIoiJbEaZWzs/30-Years-Factory-Price-Free-Sample-Name-Organic-Fertilizer.webp'
        },
        {
            'name': 'Ammounium Nitrate Fertilizer',
            'description': 'Ammonium nitrate fertilizer for healthy plants. 100% organic and eco-friendly. 20% Nitrogen, 20% Phosphorus, 20% Potassium. 100% organic.',
            'price': 8.99,
            'batches': [{'size': 6}, {'size': 12}, {'size': 24}],
            'image_url': 'https://www.shutterstock.com/image-vector/ammonium-nitrate-nh4no3-sack-bag-600nw-1790749466.jpg'
        },
    ]
    return render_template('listings/view_listings.html', products=products, user=current_user)

@listings.route('/inventory', methods=['POST'])
@login_required
def create_inventory():
    inventory = Inventory(
        name = request.form.get('name'),
        description = request.form.get('description'),
        
        user_id = current_user.id,
        user = current_user
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

@listings.route('/listings/add', methods=['POST'])
@login_required
def add_listing():
    product = Product.get('id', request.form.get('product_id'))
    listing = Listing(
        product_name = request.form.get('name'),
        description = request.form.get('description'),
        price = request.form.get('price'),
        available_stock = request.form.get('quantity'),
        min_order = request.form.get('min_order'),
    
        inventory_id = request.form.get('inventory_id'),
        inventory = Inventory.get('id', request.form.get('inventory_id')),
    
        product_id = product.id,
        product = product
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
