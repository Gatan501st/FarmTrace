from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(128))
    role = db.Column(db.String(64), default="member")
    confirmed = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # Other optional fields like first_name, last_name, bio, etc.

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = "member"  # Default role
        self.confirmed = False  # Email confirmation status
        self.avatar = None  # Default avatar path or URL
        self.last_seen = datetime.utcnow()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_online(self):
        # Implement logic to check if the user is currently online
        pass

    def login(self):
        # Implement login functionality, update last_seen timestamp, etc.
        pass

    def logout(self):
        # Implement logout functionality
        pass

    def check_permission(self, permission):
        # Implement logic to check if the user has a specific permission based on role
        pass

    def update_password(self, new_password):
        # Implement logic to update user password securely
        pass

    def send_email_confirmation(self):
        token = self.generate_confirmation_token()
        # Send email code here (placeholder function)

    def update_email(self, new_email):
        self.email = new_email
        self.confirmed = False
        db.session.add(self)
        db.session.commit()

        # Send confirmation email with token
        self.send_email_confirmation()

    def update_avatar(self, avatar_file):
        # Implement logic to update user's avatar
        pass

    def update_profile(self, **kwargs):
        # Implement logic to update other profile details like first name, last name, bio, etc.
        pass

    def generate_confirmation_token(self):
        s = Serializer(
            current_app.config["SECRET_KEY"], expires_in=3600
        )  # Token expires in 1 hour (3600 seconds)
        return s.dumps({"confirm": self.id}).decode("utf-8")

    @staticmethod
    def verify_confirmation_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return False

        # Retrieve user ID from token payload
        user_id = data.get("confirm")
        if user_id is None:
            return False

        # Fetch user from database based on user_id
        user = User.query.get(user_id)
        if user is None:
            return False

        # Mark user's email as confirmed
        user.confirmed = True
        db.session.commit()

        return True

    @staticmethod
    def send_email(subject, sender, recipients, text_body, html_body):
        # Placeholder function to send emails; replace with proper implementation
        print(f"Email sent to {recipients} with subject: {subject}")
