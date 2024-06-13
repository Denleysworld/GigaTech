from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    ItemID = Column(Integer, primary_key=True, autoincrement=True)
    ItemName = Column(String, nullable=False)
    Quantity = Column(Integer, nullable=False)
    Price = Column(Float, nullable=False)

class Customer(Base):
    __tablename__ = 'customers'
    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerName = Column(String, nullable=False)
    Email = Column(String, nullable=False)
    Phone = Column(String)

class Order(Base):
    __tablename__ = 'orders'
    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey('customers.CustomerID'))
    ItemID = Column(Integer, ForeignKey('items.ItemID'))
    OrderDate = Column(Date)
    Quantity = Column(Integer, nullable=False)
    customer = relationship("Customer", back_populates="orders")
    item = relationship("Item", back_populates="orders")

Customer.orders = relationship("Order", order_by=Order.OrderID, back_populates="customer")
Item.orders = relationship("Order", order_by=Order.OrderID, back_populates="item")

# Create a SQLite database
engine = create_engine('sqlite:///gigatech.db')
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)
# Create a session
session = Session()
