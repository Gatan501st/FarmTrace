import json
import csv
import os
from flask import render_template, request, redirect, flash, make_response, url_for, abort
from flask_login import login_required, current_user
from datetime import datetime
from app.models import Product, Batch, db
from flask import current_app
from app.decorators import role_required

from . import products
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError


@products.route('/', methods=['POST'])
def add_product():
    print(request.form.to_dict())
    product = Product(
        name=request.form.get('name'),
        description=request.form.get('description'),

        manufacturer_id=current_user.id,
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
        batch_number=request.form.get('batch_number'),
        # qrcode = request.form.get('batch_number'),
        manufacture_date=datetime.strptime(
            request.form.get('manufacture_date'), '%Y-%m-%d'),
        expiry_date=datetime.strptime(
            request.form.get('expiry_date'), '%Y-%m-%d'),
        size=request.form.get('size'),
        measurement=request.form.get('measurement'),

        product_id=product.id,
        product=product
    )
    batch.save()
    if not Batch.get('id', batch.id):
        flash('Error adding batch', 'error')
        return redirect(url_for('products.view_product', product_id=product.id))
    flash('Batch created successfully', 'success')
    return redirect(url_for('products.view_product', product_id=product.id))


@products.route('/<product_id>/batch/upload', methods=['POST'])
def batch_upload(product_id):
    product = Product.get('id', product_id)
    if product is None:
        return make_response({'message': 'Product not found'}), 404
    batches = request.files.get('batch_csv')
    if not batches or not batches.filename.split('.')[1] == 'csv':
        return make_response({'message': 'Invalid file format'}), 400
    TEMP_FOLDER = 'app/static/temp'
    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)
    file_path = f'{TEMP_FOLDER}/{secure_filename(batches.filename)}'
    batches.save(file_path)
    if not batches or not batches.filename.split('.')[1] == 'csv':
        abort(400)
    num_saved = 0
    with open(file_path, 'r', newline="") as f:
        values = csv.reader(f)
        total_batches = len(values)
        for value in values:
            try:
                batch = Batch(
                    batch_number=value[0],
                    manufacture_date=datetime.strptime(
                        value[1], '%Y-%m-%d'),
                    expiry_date=datetime.strptime(value[2], '%Y-%m-%d'),
                    size=value[3],
                    measurement=value[4],

                    product_id=product_id,
                    product=product
                )
                batch.save()
                num_saved += 1
            except IndexError:
                pass
            except IntegrityError:
                os.remove(file_path)
                return make_response({'message': 'Failed: Similar batch numbers detected'}), 409
    os.remove(file_path)
    return make_response({'message': f'Added {num_saved} out of {total_batches} batches'}), 201
