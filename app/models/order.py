from app import db

class Order(db.Model):
    __tablename__ = 'orders'
    product_id = db.Column(db.String(64), db.ForeignKey('products.id'))
    product = db.relationship('Product', back_populates='orders')
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='orders')
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)
    status = db.Column(db.String(64))
    order_date = db.Column(db.DateTime)
    delivery_date = db.Column(db.DateTime)
    order_number = db.Column(db.String(64))
    payment_method = db.Column(db.String(64))
    payment_status = db.Column(db.String(64))
    delivery_status = db.Column(db.String(64))
    delivery_address = db.Column(db.String(128))
    
    def __repr__(self):
        return f'<Order {self.order_number}>'