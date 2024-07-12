from flask import render_template, redirect, url_for, request
from app.main import main

@main.route('/cart')
def cart_view():
    total = sum(item['product']['price'] * item['quantity'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@main.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = int(request.form['quantity'])
    for item in cart:
        if item['product']['id'] == product_id:
            item['quantity'] = quantity
            break
    return redirect(url_for('main.cart_view'))

@main.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    global cart
    cart = [item for item in cart if item['product']['id'] != product_id]
    return redirect(url_for('main.cart_view'))