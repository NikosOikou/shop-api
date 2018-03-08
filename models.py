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
