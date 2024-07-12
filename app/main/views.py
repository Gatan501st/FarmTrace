import os
from datetime import datetime
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from app.main import main
from app.models.user import User
from app.email import send_confirmation_email, confirm_token


@main.route("/")
def index():
    return render_template("main/index.html")


@main.route("/about-us")
def about_us():
    return render_template("main/about_us.html")


@main.route("/how-it-works")
def how_it_works():
    return render_template("main/how_it_works.html")

@main.route('/home')
def home():
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
    return render_template('main/home.html', products=products)

@main.route("/contact-us")
def contact_us():
    return render_template("main/contact_us.html")

@main.route('/verify_email', methods=['GET', 'POST'])
@login_required
def verify_email():
    if request.method == 'POST':
        send_confirmation_email(current_user.email)
        flash('Email sent. Check your inbox', 'success')
    return render_template('email/email_sent.html')

@main.route('/confirm/<token>')
def confirm_token(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('index'))
    
    user = User.query.filter_by(email=email).first_or_404()
    
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        user.save()
        flash('You have confirmed your account. Thanks!', 'success')
    
    return redirect(url_for('accounts.sign_in'))
