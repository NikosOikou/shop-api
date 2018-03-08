import json
import unittest

from models import Customer, connect_to_db, db
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

    def test_get_shop(self):
        """Test retrieving shop item from db"""
        customer = Customer(name="John")

        db.session.add(customer)
        db.session.commit()

        result = self.client.get('/customer/1')
        self.assertEqual(result.status_code, 200)

        data = json.loads(result.data)
        self.assertEqual(data['name'], 'John')

    def test_post_shop(self):
        """Test posting a shop item"""

        result = self.client.post('/customer/',
                                  data=json.dumps({'name': 'John'}),
                                  content_type='application/json')

        self.assertEqual(result.status_code, 200)

        # Check for the item in the db
        shop = Customer.query.first()
        self.assertEqual(shop.name, 'John')


if __name__ == '__main__':
    unittest.main()
