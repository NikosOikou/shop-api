from flask import Flask, abort
from flask_restful import Api, Resource, fields, marshal_with, reqparse

from models import Customer, connect_to_db, db

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


class CustomerView(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name',
                                 type=str,
                                 required=True,
                                 help='No name provided',
                                 location='json')
    customer_fields = {
        'id': fields.Integer,
        'name': fields.String,
    }

    @marshal_with(customer_fields)
    def get(self, customer_id):
        """Retrieve a customer item by id"""

        customer = Customer.query.get(customer_id)

        if not customer:
            abort(404, "customer_id: {} not found".format(customer_id))

        return customer

    @marshal_with(customer_fields)
    def post(self):
        """Create a new customer item"""

        args = self.parser.parse_args()

        customer = Customer(name=args['name'])

        db.session.add(customer)
        db.session.commit()

        return customer

    @marshal_with(customer_fields)
    def put(self, customer_id):
        """Update a customer item"""

        args = self.parser.parse_args()

        customer = Customer.query.get(customer_id)

        if not customer:
            abort(404, "customer_id: {} not found".format(customer_id))

        customer.name = args['name']
        db.session.commit()

        return customer


api.add_resource(CustomerView,
                 '/customer/',
                 '/customer/<int:customer_id>')


if __name__ == '__main__':

    connect_to_db(app)
    app.run(debug=True)
