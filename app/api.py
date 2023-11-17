from flask import Blueprint, jsonify, request, current_app
from app.models import db, Customer, Account


api = Blueprint('api', __name__)


@api.route('/test-api', methods=['POST'])
def my_test_api():
    return jsonify({})

# Create a new customer
@api.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    name = data['name']
    customer = Customer(name=name)
    db.session.add(customer)
    db.session.commit()
    return jsonify({'id': customer.id, 'name': customer.name}), 201

# Retrieve all customers
@api.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in customers])

# Retrieve a specific customer
@api.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify({'id': customer.id, 'name': customer.name})

# Create a new account
@api.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    customer_id = data['customer_id']
    customer = Customer.query.get_or_404(customer_id)
    balance = data.get('balance', 0)
    account = Account(customer=customer, balance=balance)
    db.session.add(account)
    db.session.commit()
    return jsonify({'id': account.id, 'customer_id': customer_id, 'balance': account.balance}), 201

# Retrieve all accounts
@api.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()
    return jsonify([{'id': a.id, 'customer_id': a.customer.id, 'customer_name': a.customer.name, 'balance': a.balance} for a in accounts])

# Retrieve a specific account
@api.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = Account.query.get_or_404(account_id)
    return jsonify({'id': account.id, 'customer_id': account.customer.id, 'customer_name': account.customer.name, 'balance': account.balance})

# Transfer money between two accounts
@api.route('/transfers', methods=['POST'])
def transfer_money():
    data = request.get_json()
    from_account_id = data['from_account_id']
    to_account_id = data['to_account_id']
    amount = data['amount']

    from_account = Account.query.get_or_404(from_account_id)
    to_account = Account.query.get_or_404(to_account_id)

    if from_account.balance < amount:
        return jsonify({'message': 'Insufficient balance in source account'}), 400

    from_account.balance -= amount
    to_account.balance += amount

    db.session.commit()

    return jsonify({'message': 'Transfer successful', 'from_account_id': from_account_id, 'to_account_id': to_account_id, 'amount': amount}), 200

