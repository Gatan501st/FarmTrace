from flask import url_for, render_template, current_app, abort, Response
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app import mail
from socket import gaierror

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration,
        )
        return email
    except (BadSignature, SignatureExpired):
        return None

def send_email(to, subject, template):
    msg = Message(subject, recipients=[to], html=template, sender=current_app.config['MAIL_DEFAULT_SENDER'])
    try:
        mail.send(msg)
    except gaierror as e:
        print(f"Email sending error: {e}")
        abort(500)

def send_confirmation_email(user_email):
    token = generate_confirmation_token(user_email)
    confirm_url = url_for('accounts.verify_token', token=token, _external=True)
    html = render_template('email/confirm.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(user_email, subject, html)
