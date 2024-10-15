from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Pizza, Ingredient, Drink, Dessert, Order, order_pizzas, order_drinks
from order import OrderStatusTracker


class PizzaService:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.order_status_tracker = OrderStatusTracker(db_url)

    def fetch_pizzas(self):
        try:
            pizzas = self.session.query(Pizza).all()
            print("Querying worked")
            return pizzas
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def add_pizza(self, name, is_vegetarian, is_vegan, price):
        new_pizza = Pizza(
            name=name,
            is_vegetarian=is_vegetarian,
            is_vegan=is_vegan,
            price=price
        )
        self.session.add(new_pizza)
        self.session.commit()
        print(f"Pizza '{name}' added successfully!")

    def update_pizza(self, pizza_id, name=None, is_vegetarian=None, is_vegan=None, price=None):
        try:
            pizza = self.session.query(Pizza).filter_by(Id=pizza_id).one()
            if name is not None:
                pizza.name = name
            if is_vegetarian is not None:
                pizza.is_vegetarian = is_vegetarian
            if is_vegan is not None:
                pizza.is_vegan = is_vegan
            if price is not None:
                pizza.price = price
            self.session.commit()
            print(f"Pizza '{pizza_id}' updated successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def delete_pizza(self, pizza_id):
        try:
            pizza = self.session.query(Pizza).filter_by(Id=pizza_id).one()
            self.session.delete(pizza)
            self.session.commit()
            print(f"Pizza '{pizza_id}' deleted successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")

    def fetch_ingredients(self):
        try:
            ingredients = self.session.query(Ingredient).all()
            return ingredients
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def fetch_drinks(self):
        try:
            drinks = self.session.query(Drink).all()
            return drinks
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def fetch_desserts(self):
        try:
            desserts = self.session.query(Dessert).all()
            return desserts
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def calculate_pizza_price(self, pizza_id):
        try:
            pizza = self.session.query(Pizza).filter_by(Id=pizza_id).one()
            ingredient_cost = sum(ingredient.price for ingredient in pizza.ingredients)
            profit_margin = 0.40
            vat = 0.09
            price = ingredient_cost * (1 + profit_margin) * (1 + vat)
            return price
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def fetch_dietary_info(self, pizza_id):
        try:
            pizza = self.session.query(Pizza).filter_by(Id=pizza_id).one()
            is_vegetarian = all(ingredient.is_vegetarian for ingredient in pizza.ingredients)
            is_vegan = all(ingredient.is_vegan for ingredient in pizza.ingredients)
            return {'is_vegetarian': is_vegetarian, 'is_vegan': is_vegan}
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def create_order(self, customer_id, pizzas, drinks, desserts, is_discount_applied, total_price):
        order_count = self.order_status_tracker.get_order_count(customer_id)
        discount = 0.1 if order_count % 10 == 0 or self.order_status_tracker.is_birthday else 0.0
        new_order = Order (
            order_date=datetime.now(),
            customer_id=customer_id,
            is_discount_applied=is_discount_applied,
            total_price=total_price * (1-discount),
            status = "Pending"
        )
        self.session.add(new_order)
        self.session.commit()

        for pizza in pizzas:
            self.session.execute(order_pizzas.insert().values(order_id = new_order.id, pizza_id = pizza.Id))
        for drink in drinks:
            self.session.execute(order_drinks.insert().values(order_id = new_order.id, drink_id = drink.Id))

    def cancel_order(self, order_id):
        if self.order_status_tracker.cancel_order(order_id):
            try:
                order = self.session.query(Order).filter_by(Id = order_id).one()
                self.session.delete(order)
                self.session.commit()
                return True
            except Exception as e:
                print(f"An error occurred: {e}")
                return False
        else:
            return False
