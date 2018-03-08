from flask import Flask, abort
from flask_restful import Api, Resource, fields, marshal_with, reqparse

from models import Customer, Order, Product, connect_to_db, db

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


class ProductView(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('ean',
                                 type=str,
                                 required=True,
                                 help='No product ean provided',
                                 location='json')
        self.parser.add_argument('stock',
                                 type=int,
                                 required=True,
                                 help='No product stock provided',
                                 location='json')

    product_fields = {
        'id': fields.Integer,
        'ean': fields.String,
        'stock': fields.Integer,
    }

    @marshal_with(product_fields)
    def get(self, product_id):
        """Retrieve a product item by id"""

        product = Product.query.get(product_id)

        if not product:
            abort(404, "product_id: {} not found".format(product_id))

        return product

    @marshal_with(product_fields)
    def post(self):
        """Create a new product item"""

        args = self.parser.parse_args()

        product = Product(ean=args['ean'], stock=args['stock'])

        db.session.add(product)
        db.session.commit()

        return product

    @marshal_with(product_fields)
    def put(self, product_id):
        """Update a product item"""

        args = self.parser.parse_args()

        product = Product.query.get(product_id)

        if not product:
            abort(404, "product_id: {} not found".format(product_id))

        product.ean = args['ean']
        product.stock = args['stock']
        db.session.commit()

        return product


api.add_resource(ProductView,
                 '/product/',
                 '/product/<int:product_id>')


class OrderView(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('customer_id',
                                 type=int,
                                 required=True,
                                 help='No customer_id provided',
                                 location='json')
        self.parser.add_argument('product_id',
                                 type=int,
                                 required=True,
                                 help='No prodcut_id provided',
                                 location='json')

    order_fields = {
        'id': fields.Integer,
        'customer_id': fields.Integer,
        'product_id': fields.Integer,
        'accepted': fields.Boolean,
    }

    @marshal_with(order_fields)
    def get(self, order_id):
        """Retrieve an order item by id"""

        order = Order.query.get(order_id)

        if not order:
            abort(404, "order_id: {} not found".format(order_id))

        return order

    @marshal_with(order_fields)
    def post(self):
        """Create a new order item"""

        args = self.parser.parse_args()

        customer = Customer.query.get(args['customer_id'])

        if not customer:
            abort(404, "customer_id: {} not found".format(args['customer_id']))

        product = Product.query.get(args['product_id'])

        if not product:
            abort(404, "product_id: {} not found".format(args['product_id']))

        order = Order(
            customer_id=args['customer_id'],
            product_id=args['product_id'],
            accepted=product.stock != 0
        )

        db.session.add(order)
        db.session.commit()

        return order

    @marshal_with(order_fields)
    def put(self, order_id):
        """Update an order item"""

        args = self.parser.parse_args()

        order = Order.query.get(order_id)

        if not order:
            abort(404, "order_id: {} not found".format(order_id))

        customer = Customer.query.get(args['customer_id'])

        if not customer:
            abort(404, "customer_id: {} not found".format(args['customer_id']))

        product = Product.query.get(args['product_id'])

        if not product:
            abort(404, "product_id: {} not found".format(args['product_id']))

        order.customer_id = args['customer_id']
        order.product_id = args['product_id']
        order.accepted = product.stock != 0
        db.session.commit()

        return order


api.add_resource(OrderView,
                 '/order/',
                 '/order/<int:order_id>')


if __name__ == '__main__':

    connect_to_db(app)
    app.run(debug=True)
