from app.models import Customer, Account, db
from tests import clear_session

def test_create_account(client):
    
    # Create a customer
    customer = Customer(name='John Doe')
    db.session.add(customer)
    db.session.commit()

    # Create an account
    data = {'customer_id': customer.id, 'balance': 1000}
    response = client.post('/accounts', json=data)

    # Check the response
    assert response.status_code == 201
    assert response.json == {'id': 1, 'customer_id': customer.id, 'balance': 1000}

    # Check that the account was created in the database
    account = Account.query.get(1)
    assert account.customer == customer
    assert account.balance == 1000

    # Clear the session to avoid affecting other tests
    clear_session()

def test_get_accounts(client):
    # Create some customers and accounts
    customer1 = Customer(name='John Doe')
    customer2 = Customer(name='Jane Smith')
    account1 = Account(customer=customer1, balance=1000)
    account2 = Account(customer=customer2, balance=2000)
    db.session.add_all([customer1, customer2, account1, account2])
    db.session.commit()

    # Retrieve all accounts
    response = client.get('/accounts')

    # Check the response
    assert response.status_code == 200
    assert response.json == [{'id': account1.id, 'customer_id': customer1.id, 'customer_name': 'John Doe', 'balance': 1000},
                             {'id': account2.id, 'customer_id': customer2.id, 'customer_name': 'Jane Smith', 'balance': 2000}]

    # Clear the session to avoid affecting other tests
    clear_session()

def test_get_account(client):
    # Create a customer and an account
    customer = Customer(name='John Doe')
    account = Account(customer=customer, balance=1000)
    db.session.add_all([customer, account])
    db.session.commit()

    # Retrieve the account
    response = client.get(f'/accounts/{account.id}')

    # Check the response
    assert response.status_code == 200
    assert response.json == {'id': account.id, 'customer_id': customer.id, 'customer_name': 'John Doe', 'balance': 1000}

    # Clear the session to avoid affecting other tests
    clear_session()