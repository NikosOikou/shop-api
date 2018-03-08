# shop-api
A dumbed down, online shop REST API that performs CRUD operations on a SQLite database using Flask and the extension, Flask-RESTful.

## Contents:
**shop.py** - Defines the flask app, and the Flask RESTful api endpoints defined on top of it     
**models.py** - Defines the data model, implemented with the Flask SQLAlchemy ORM    
**tests.py** - Testing of API endpoints using Python unittest module

## Using the api:
To access the api from the command line:

GET request (for customer with id 1):
```
curl http://localhost:5000/customer/1
```

POST request (for customer with name 'John')
```
curl http://localhost:5000/customer/ -X POST -H "Content-Type:application/json" -d '{"name":"John"}'
```

## Tests
To run the tests:

```
python tests.py
```
