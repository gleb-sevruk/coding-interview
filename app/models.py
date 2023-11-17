from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    accounts = relationship('Account', back_populates='customer')

    def __repr__(self):
        return f"Customer(id={self.id}, name='{self.name}')"

 
class Account(db.Model):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    balance = Column(Float, nullable=False, default=0)

    customer = relationship('Customer', back_populates='accounts')
    
    def __repr__(self):
        return f"Account(id={self.id}, customer_id={self.customer_id}, balance={self.balance})"

    def deposit(self, amount: float):
        self.balance -= amount

    def withdraw(self, amount: float):
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount