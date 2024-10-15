from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import bcrypt

Base = declarative_base()

class Rider(Base):
    __tablename__ = "riders"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    available = Column(String, default=True)

class Pizza(Base):
    __tablename__ = 'pizzas'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    is_vegetarian = Column(Boolean, name='IsVegetarian', nullable=False)
    is_vegan = Column(Boolean, name='IsVegan', nullable=False)
    price = Column(Float, name='Price', nullable=False)

class Ingredient(Base):
    __tablename__ = 'ingredients'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cost = Column(Float, name='Cost', nullable=False)
    is_vegetarian = Column(Boolean, name='IsVegitarian', nullable=False)
    is_vegan = Column(Boolean, name='IsVegan', nullable=False)

class Drink(Base):
    __tablename__ = 'drinks'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, name='Price', nullable=False)

class Dessert(Base):
    __tablename__ = 'desserts'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, name='Price', nullable=False)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True, name='Id')
    name = Column(String, name='Name', nullable=False)
    gender = Column(String, name='Gender', nullable=False)
    birthdate = Column(DateTime, name='Birthdate', nullable=False)
    address = Column(String, name='Address', nullable=False)
    password = Column(String, name='Password', nullable=False)

    def set_pw(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_pw(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True, autoincrement=True, name='Id')
    name = Column(String, name='Name', nullable=False)
    gender = Column(String, name='Gender', nullable=False)
    password = Column(String, name='Password', nullable=False)

    def set_pw(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    def check_pw(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True, name='Id')
    order_date = Column(DateTime, name='OrderDate', nullable=False)
    customer_name = Column(String, name='CustomerName', nullable=False)
    customer_gender = Column(String, name='CustomerGender', nullable=False)
    customer_birthdate = Column(DateTime, name='CustomerBirthdate', nullable=False)
    customer_phone = Column(String, name='CustomerPhone', nullable=False)
    customer_address = Column(String, name='CustomerAddress', nullable=False)
    is_discount_applied = Column(Boolean, name='IsDiscountApplied', nullable=False)
    total_price = Column(Float, name='TotalPrice', nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.Id'), name='CustomerId', nullable=True)
    customer = relationship('Customer')
    status = Column(String, name='Status', default='Pending', nullable=False)
    rider_id = Column(Integer, ForeignKey("riders.id"))
    rider = relationship("Rider", backref="orders")
    assigned_time = Column(DateTime)

class DeliveryPerson(Base):
    __tablename__ = 'delivery_persons'
    id = Column(Integer, primary_key=True, autoincrement=True, name='Id')
    name = Column(String, nullable=False)
    postal_code = Column(String, name='PostalCode', nullable=False)
    available = Column(Boolean, default=True)

# Many-to-Many relationships
pizza_ingredients = Table('pizzaingredients', Base.metadata,
    Column('PizzaId', Integer, ForeignKey('pizzas.Id'), primary_key=True),
    Column('IngredientId', Integer, ForeignKey('ingredients.Id'), primary_key=True)
)

order_pizzas = Table('orderpizzas', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.Id'), primary_key=True),
    Column('pizza_id', Integer, ForeignKey('pizzas.Id'), primary_key=True)
)

order_drinks = Table('orderdrinks', Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.Id'), primary_key=True),
    Column('drink_id', Integer, ForeignKey('drinks.Id'), primary_key=True)
)