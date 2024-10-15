from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import bcrypt

Base = declarative_base()

pizza_ingredients = Table('pizzaingredients', Base.metadata,
    Column('PizzaId', Integer, ForeignKey('pizzas.Id'), primary_key=True),
    Column('IngredientId', Integer, ForeignKey('ingredients.Id'), primary_key=True)
)

order_pizzas = Table('orderpizzas', Base.metadata,
    Column('OrderId', Integer, ForeignKey('orders.Id'), primary_key=True),
    Column('PizzaId', Integer, ForeignKey('pizzas.Id'), primary_key=True)
)

order_drinks = Table('orderdrinks', Base.metadata,
    Column('OrderId', Integer, ForeignKey('orders.Id'), primary_key=True),
    Column('DrinkId', Integer, ForeignKey('drinks.Id'), primary_key=True)
)

order_desserts = Table('orderdesserts', Base.metadata,
    Column('OrderId', Integer, ForeignKey('orders.Id'), primary_key=True),
    Column('DessertId', Integer, ForeignKey('desserts.Id'), primary_key=True)
)

class Pizza(Base):
    __tablename__ = 'pizzas'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    is_vegetarian = Column(Boolean, name='IsVegetarian', nullable=False)
    is_vegan = Column(Boolean, name='IsVegan', nullable=False)
    price = Column(Float, name='Price', nullable=False)

    ingredients = relationship('Ingredient', secondary=pizza_ingredients, back_populates='pizzas')
    orders = relationship('Order', secondary=order_pizzas, back_populates='pizzas')

class Ingredient(Base):
    __tablename__ = 'ingredients'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    cost = Column(Float, name='Cost', nullable=False)
    is_vegetarian = Column(Boolean, name='IsVegetarian', nullable=False)
    is_vegan = Column(Boolean, name='IsVegan', nullable=False)

    pizzas = relationship('Pizza', secondary=pizza_ingredients, back_populates='ingredients')

class Drink(Base):
    __tablename__ = 'drinks'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, name='Price', nullable=False)

    orders = relationship('Order', secondary=order_drinks, back_populates='drinks')

class Dessert(Base):
    __tablename__ = 'desserts'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, name='Price', nullable=False)

    orders = relationship('Order', secondary=order_desserts, back_populates='desserts')

class Customer(Base):
    __tablename__ = 'customers'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, name='Name', nullable=False)
    gender = Column(String, name='Gender', nullable=False)
    birthdate = Column(DateTime, name='Birthdate', nullable=False)
    address = Column(String, name='Address', nullable=False)
    password = Column(String, name='Password', nullable=False)

    orders = relationship('Order', back_populates='customer')

    def set_pw(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_pw(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class DeliveryPersonnel(Base):
    __tablename__ = 'delivery_personnel'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    postalCode = Column(String, nullable=False)
    available = Column(Boolean, nullable=False)

class Admin(Base):
    __tablename__ = 'admins'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, name='Name', nullable=False)
    gender = Column(String, name='Gender', nullable=False)
    password = Column(String, name='Password', nullable=False)

    def set_pw(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_pw(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

class Order(Base):
    __tablename__ = 'orders'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime, name='OrderDate', nullable=False)
    customer_name = Column(String, name='CustomerName', nullable=False)
    customer_gender = Column(String, name='CustomerGender', nullable=False)
    customer_birthdate = Column(DateTime, name='CustomerBirthdate', nullable=False)
    customer_phone = Column(String, name='CustomerPhone', nullable=False)
    customer_address = Column(String, name='CustomerAddress', nullable=False)
    is_discount_applied = Column(Boolean, name='IsDiscountApplied', nullable=False)
    total_price = Column(Float, name='TotalPrice', nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.Id'), name='CustomerId', nullable=True)
    status = Column(String, name='Status', default='Pending', nullable=False)

    customer = relationship('Customer', back_populates='orders')
    pizzas = relationship('Pizza', secondary=order_pizzas, back_populates='orders')
    drinks = relationship('Drink', secondary=order_drinks, back_populates='orders')
    desserts = relationship('Dessert', secondary=order_desserts, back_populates='orders')


