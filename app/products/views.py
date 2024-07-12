import json, csv
from flask import render_template, request, redirect, flash, make_response, url_for, abort
from flask_login import login_required, current_user
from datetime import datetime
from app.models import Product, Batch, db
from flask import current_app
from app.decorators import role_required

from . import products

@products.route('/', methods=['POST'])
def add_product():
    batches = request.form.get('batch_sizes')[1:-1].split(',')
    for batch in batches:
        print(batches)
        batch = float(batch)
    batches = json.dumps(batches)
    product = Product(
        name = request.form.get('name'),
        description = request.form.get('description'),
        batch_sizes = batches,
        manufacturer = current_user,
    )
    product.save()
    if not Product.get('id', product.id):
        flash('Error adding product', 'error')
        return redirect(url_for('accounts.dashboard'))
    flash('Product added successfully', 'success')
    return redirect(url_for('accounts.dashboard'))


@products.route("/<product_id>")
@login_required
@role_required('Manufacturer')
def view_product(product_id):
    product = db.session.query(Product).filter_by(id=product_id).first()
    if product:
        return render_template('products/view_product.html', product=product)
    else:
        return make_response({"error": 'Product not found'}), 404


@products.route('/<product_id>/batch/add', methods=['POST'])
def add_batch(product_id):
    product = Product.get('id', product_id)
    if not product:
        flash("Error fetching product")
        return make_response(), 409
    batch = Batch(
        batch_number = request.form.get('batch_number'),
        # qrcode = request.form.get('batch_number'),
        manufacture_date = datetime.strptime(request.form.get('manufacture_date'), '%Y-%m-%d'),
        expiry_date = datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d'),
        size = request.form.get('size'),
        
        product_id = product.id,
        product = product
    )
    batch.save()
    if not Batch.get('id', batch.id):
        flash('Error adding batch', 'error')
        return redirect(url_for('products.view_product', product_id=product.id))
    flash('Batch created successfully', 'success')
    return redirect(url_for('products.view_product', product_id=product.id))

@products.route('/<product_id>/batch/upload')
def batch_upload(product_id):
    product = Product.get('id', product_id)
    if product is None:
        return make_response({'message': 'Product not found'}), 404
    batches = request.files.get('batch_csv')
    if not batches or not batches.filename.split('.')[1] == 'csv':
        abort(400)
    with open(batches, 'r', newline="") as f:
        values = csv.reader(f)
        for value in values:
            if len(value) < 3:
                batch = Batch(
                    batch_number = value[0],
                    manufacture_date = datetime.strptime(value[1], '%Y-%m-%d'),
                    expiry_date = datetime.strptime(value[2], '%Y-%m-%d'),
                    size = value[3],
                    
                    product_id = product_id,
                    product = product.id
                )
                batch.save()
            