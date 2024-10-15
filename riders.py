import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from models import Rider, Order


class RiderManagement:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        Session = sessionmaker(bind=engine)
        self.session = Session()


    def assign_rider_to_order(self, order):

        try:
            rider = self.session.query(Rider).filter_by(available=True).first()

            if rider:
                order.rider = rider
                order.assigned_time = datetime.datetime.now()
                rider.available = False
                self.session.commit()
                return f"Rider {rider.name} assigned to order {order.id}."
            else:
                return "No riders available at the moment."

        except IntegrityError as e:
            self.session.rollback()
            return f"Error assigning rider: {e}"


    def release_rider(self,rider):
        rider.available = True
        self.session.commit()


    def process_orders(self):
        prepared_orders = self.session.query(Order).filter_by(label="prepared").all()
        for order in prepared_orders:
            if not order.rider:
                message = self.assign_rider_to_order(order)
                print(message)
            elif order.rider and order.assigned_time and (datetime.datetime.now() - order.assigned_time) > datetime.timedelta(minutes=20):
                self.release_rider(order.rider)
                print(f"Rider {order.rider.name} released from order {order.id}.")

