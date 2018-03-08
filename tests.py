import json
import unittest

from models import Customer, connect_to_db, db, Order, Product
from shop import app


class TestAPI(unittest.TestCase):
    """Tests with DB."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, 'sqlite:///test.db')

        # Create tables in testdb
        db.create_all()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_get_customer(self):
        """Test retrieving customer item from db"""
        customer = Customer(name="John")

        db.session.add(customer)
        db.session.commit()

        result = self.client.get('/customer/1')
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data)
        self.assertEqual(data['name'], 'John')

    def test_post_customer(self):
        """Test posting a customer item"""

        result = self.client.post('/customer/',
                                  data=json.dumps({'name': 'John'}),
                                  content_type='application/json')

        self.assertEqual(result.status_code, 200)

        # Check for the item in the db
        customer = Customer.query.first()
        self.assertEqual(customer.name, 'John')

    def test_get_product(self):
        """Test retrieving customer item from db"""
        product = Product(ean="123", stock=1)

        db.session.add(product)
        db.session.commit()

        result = self.client.get('/product/1')
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data)
        self.assertEqual(data['ean'], '123')
        self.assertEqual(data['stock'], 1)

    def test_post_product(self):
        """Test posting a product item"""

        result = self.client.post('/product/',
                                  data=json.dumps({'ean': '123', 'stock': 1}),
                                  content_type='application/json')

        self.assertEqual(result.status_code, 200)

        # Check for the item in the db
        product = Product.query.first()
        self.assertEqual(product.ean, '123')
        self.assertEqual(product.stock, 1)

    def test_get_order(self):
        """Test retrieving order item from db"""
        customer = Customer(name="John")
        product = Product(ean="123", stock=1)

        db.session.add(customer)
        db.session.add(product)
        db.session.commit()

        order = Order(customer_id=customer.id, product_id=product.id)

        db.session.add(order)
        db.session.commit()

        result = self.client.get('/order/1')
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data)
        self.assertEqual(data['customer_id'], 1)
        self.assertEqual(data['product_id'], 1)
        # self.assertTrue(data['accepted'])

    def test_post_order(self):
        """Test posting a order item"""
        customer = Customer(name="John")
        product = Product(ean="123", stock=1)

        db.session.add(customer)
        db.session.add(product)
        db.session.commit()

        result = self.client.post('/order/',
                                  data=json.dumps({
                                    'customer_id': 1,
                                    'product_id': 1
                                  }),
                                  content_type='application/json')

        self.assertEqual(result.status_code, 200)

        # Check for the item in the db
        order = Order.query.first()
        self.assertEqual(order.customer_id, 1)
        self.assertEqual(order.product_id, 1)
        self.assertTrue(order.accepted)


if __name__ == '__main__':
    unittest.main()
