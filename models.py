from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app, db_uri="sqlite:///shop.db"):
    """Connect the database to Flask app."""

    # Configure to use SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


class Customer(db.Model):
    """
    Create a Customer table.
    """
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    orders = db.relationship('Order', backref='customer', lazy='dynamic')


class Product(db.Model):
    """
    Create a Product table
    """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    ean = db.Column(db.String(60), unique=True)
    stock = db.Column(db.Integer)
    available = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='product', lazy='dynamic')


class Order(db.Model):
    """
    Create an Order table
    """
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    accepted = db.Column(db.Boolean, default=False)
