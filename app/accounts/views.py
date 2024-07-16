from flask import redirect, request, render_template, flash, url_for, current_app, abort, make_response
from flask_login import current_user
from flask_login import login_required, login_user, logout_user
from app.decorators import email_verified
from datetime import datetime

from app.accounts import accounts
from app.models import User, Manufacturer, Retailer, Wholesaler, Farmer, Administrator
from app.email import send_confirmation_email, confirm_token


@accounts.route("/signin", methods=["GET", "POST"])
def sign_in():
    print('here is your form')
    if current_user.is_authenticated:
        print('is authenticated')
        return redirect(url_for('main.index'))
    print('You are not authenticated')
    print(request.form.to_dict())
    if request.method == 'POST':
        print(f'Got your form: {request.form.to_dict()}')
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.get('email', email)
        print(user)
        if user and user.verify_password(password):
            print('Valid credentials')
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('accounts.dashboard')
            return redirect(next)
        flash('Invalid Credentials', 'error')
    return render_template("accounts/sign_in.html")


@accounts.route("/signup", methods=["GET", "POST"])
def sign_up():
    roles = {
        'Manufacturer': Manufacturer,
        'Retailer': Retailer,
        'Wholesaler': Wholesaler,
        'Farmer': Farmer,
        'Administrator': Administrator
    }
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.get('email', email)
        if user:
            flash('Account already exists')
        else:
            role = request.form.get('role')
            if role not in roles:
                if email.split('@')[1] == current_app.config['ORGANIZATION_DOMAIN']:
                    role = 'Administrator'
                else:
                    abort(400)
            user = roles.get(role)(
                company_name=request.form.get('company'),
                firstname=request.form.get('firstname'),
                lastname=request.form.get('lastname'),
                email=request.form.get('email'),
                password=request.form.get('password'),
                location=request.form.get('location'),
                phone=request.form.get('phone')
            )
            send_confirmation_email(user.email)
            user.save()
            flash(
                'Registration success. Check your email for a confirmation link', 'success')
            return redirect(url_for('accounts.sign_in', next=url_for('accounts.verify_email')))
    return render_template("accounts/sign_up.html")


@accounts.route('/verify_email', methods=['GET', 'POST'])
@login_required
def verify_email():
    if current_user.confirmed:
        flash('Account already verified')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        send_confirmation_email(current_user.email)
        flash('Email sent. Check your inbox', 'success')
    return render_template('email/email_sent.html')


@accounts.route('/confirm/<token>')
def verify_token(token):
    email = confirm_token(token)
    if email is None:
        flash("Invalid or expired token")
        return redirect(url_for('accounts.verify_email'))

    user = User.query.filter_by(email=email).first_or_404()

    if user.confirmed:
        flash('Account already verified', 'success')
        return redirect('accounts.sign_in')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.now()
        user.save()
        flash('You have confirmed your account. Thanks!', 'success')

    return redirect(url_for('accounts.sign_in'))


@accounts.route("/profile")
@login_required
def profile():
    return render_template('accounts/profile.html', user=current_user)

@accounts.route('profile/edit', methods=['PUT'])
def edit_profile():
    if not request.get_json() or not type(request.get_json()) == dict:
        return make_response({'message': 'Invalid form data'})
    data = request.get_json()
    print(data)
    for key, value in data.items():
        if key == 'email':
            current_user.confirmed = None
            current_user.confirmed_on = None
        setattr(current_user, key, value)
    current_user.save()
    print(current_user)
    return make_response({'message': 'Updates saved'})

@accounts.route("/dashboard")
@login_required
@email_verified
def dashboard():
    return render_template("accounts/dashboard.html", user=current_user)


@accounts.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
