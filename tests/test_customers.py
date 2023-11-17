from app.models import Customer, db
from tests import clear_session


def test_create_customer(client):
    data = {'name': 'John Doe'}
    response = client.post('/customers', json=data)
    assert response.status_code == 201
    assert response.json == {'id': 1, 'name': 'John Doe'}

    # Clear the session to avoid affecting other tests
    clear_session()


def test_get_customers(client):
    customer1 = Customer(name='John Doe')
    customer2 = Customer(name='Jane Smith')
    db.session.add_all([customer1, customer2])
    db.session.commit()

    response = client.get('/customers')
    assert response.status_code == 200
    print(response.json)
    assert len(response.json) == 2
    assert response.json[0]['name'] == 'John Doe'
    assert response.json[1]['name'] == 'Jane Smith'

    # Clear the session to avoid affecting other tests
    clear_session()


def test_get_customer(client):
    customer = Customer(name='John Doe')
    db.session.add(customer)
    db.session.commit()

    response = client.get(f'/customers/{customer.id}')
    assert response.status_code == 200
    assert response.json == {'id': customer.id, 'name': 'John Doe'}

    # Clear the session to avoid affecting other tests
    clear_session()