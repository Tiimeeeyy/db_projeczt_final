from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Customer, Order

# This class handles all
class CustomerHandling:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        session = sessionmaker(bind=engine)
        self.session = session()

    def register_customer(self, name, gender, birthdate, address, password):
        new_customer = Customer(
            name = name,
            gender=gender,
            birthdate=birthdate,
            address=address
        )
        new_customer.set_pw(password)
        self.session.add(new_customer)
        self.session.commit()
        print(f"Customer '{name} registered successfully")

    def login_customer(self,name, password):
        customer = self.session.query(Customer).filter_by(name=name).first()
        if customer and customer.check_pw(password):
            print(f"Customer '{name}' logged in successfully")
            return True
        else:
            print("Invalid name or Password")
            return False
        

    def send_order_confirmation(self, order_id, customer_email):
        try:
            order = self.session.query(Order).filter_by(Id=order_id).one()
            estimated_delivery_time = self.calculate_estimated_delivery_time(order_id)
            order_details = f"Order ID: {order_id}\nTotal Price: {order.total_price}\nEstimated Delivery Time: {estimated_delivery_time}"
            self.send_email(customer_email, "Order Confirmation", order_details)
            print(f"Order confirmation sent to {customer_email}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def calculate_estimated_delivery_time(order_id):
        # Logic to calculate estimated delivery time
        return "30 minutes"

    def send_email(self, customer_email, param, order_details):
        pass