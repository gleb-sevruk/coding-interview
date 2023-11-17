from app.models import Customer, Account, db
from tests import clear_session

def test_transfer_money_insufficient_balance(client):
    # Create two accounts
    customer1 = Customer(name='John Doe')
    customer2 = Customer(name='Jane Smith')
    account1 = Account(customer=customer1, balance=100)
    account2 = Account(customer=customer2, balance=0)
    db.session.add_all([customer1, customer2, account1, account2])
    db.session.commit()

    # Try to transfer more money than is available in the source account
    data = {'from_account_id': account1.id, 'to_account_id': account2.id, 'amount': 200}
    response = client.post('/transfers', json=data)
    assert response.status_code == 400
    assert response.json == {'message': 'Insufficient balance in source account'}

    # Verify that the balances have not changed
    db.session.refresh(account1)
    db.session.refresh(account2)
    assert account1.balance == 100
    assert account2.balance == 0

    # Clear the session to avoid affecting other tests
    clear_session()

def test_transfer_money_successful(client):
    # Create two accounts
    customer1 = Customer(name='John Doe')
    customer2 = Customer(name='Jane Smith')
    account1 = Account(customer=customer1, balance=100)
    account2 = Account(customer=customer2, balance=0)
    db.session.add_all([customer1, customer2, account1, account2])
    db.session.commit()

    # Transfer money from account 1 to account 2
    data = {'from_account_id': account1.id, 'to_account_id': account2.id, 'amount': 40}
    response = client.post('/transfers', json=data)
    assert response.status_code == 200
    assert response.json == {'message': 'Transfer successful', 'from_account_id': account1.id, 'to_account_id': account2.id, 'amount': 40}

    # Verify that the balances have been updated
    db.session.refresh(account1)
    db.session.refresh(account2)
    assert account1.balance == 60
    assert account2.balance == 40

    # Clear the session to avoid affecting other tests
    clear_session()

def test_transfer_money_multiple_attempts(client):
    # Create a customer and two accounts
    customer = Customer(name='John Doe')
    account1 = Account(customer=customer, balance=1000)
    account2 = Account(customer=customer, balance=0)
    db.session.add_all([customer, account1, account2])
    db.session.commit()

    # Transfer money from account1 to account2
    data = {'from_account_id': account1.id, 'to_account_id': account2.id, 'amount': 500}
    response = client.post('/transfers', json=data)
    assert response.status_code == 200
    assert response.json == {'message': 'Transfer successful', 'from_account_id': account1.id, 'to_account_id': account2.id, 'amount': 500}

    # Check account balances
    assert account1.balance == 500
    assert account2.balance == 500

    # Transfer more money than balance
    data = {'from_account_id': account1.id, 'to_account_id': account2.id, 'amount': 1000}
    response = client.post('/transfers', json=data)
    assert response.status_code == 400
    assert response.json == {'message': 'Insufficient balance in source account'}

    # Check account balances again
    assert account1.balance == 500
    assert account2.balance == 500

    # Transfer money to non-existent account
    data = {'from_account_id': account1.id, 'to_account_id': 9999, 'amount': 100}
    response = client.post('/transfers', json=data)
    assert response.status_code == 404

    # Check account balances again
    assert account1.balance == 500
    assert account2.balance == 500

    # Clear the session to avoid affecting other tests
    clear_session()