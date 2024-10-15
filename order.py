import threading
import time
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Order, Customer


class OrderStatusTracker:
	def __init__(self, db_url):
		engine = create_engine(db_url)
		Session = sessionmaker(bind=engine)
		self.session = Session()
		self.status_map = {5: "Preparing", 20: "Prepared", 30: "Out for Delivery", 40: "Delivered"}

	def start_tracking(self, order_id):
		threading.Thread(target=self._update_status, args=(order_id), daemon=True).start()

	def _update_status(self, order_id):
		while True:
			time.sleep(60)
			order = self.session.query(Order).filter_by(Id=order_id).one()
			elapsed_time = (datetime.now() - order.order_date).total_seconds() / 60
			for time_limit, status in self.status_map.items():
				if elapsed_time < time_limit:
					order.status = status
					self.session.commit()
					break
			else:
				order.status = "Delivered"
				self.session.commit()
				break

	def get_order_status(self, order_id):
		order = self.session.query(Order).filter_by(id=order_id).one()
		return order.status

	def cancel_order(self, order_id):
		order = self.session.query(Order).filter_by(Id=order_id).one()
		elapsed_time = (datetime.now() - order.order_date).total_seconds() / 60
		cancellation_limit = min(self.status_map.keys())
		if elapsed_time < cancellation_limit:
			order.status = "Cancelled"
			self.session.commit()
			return True
		return False

	def get_order_count(self, customer_id):
		return self.session.query(Order).filter_by(customer_id=customer_id).count()

	def is_birthday(self, customer_id):
		customer = self.session.query(Customer).filter_by(customer_id=customer_id).one
		today = datetime.now().date()
		return customer.birthdate.month == today.month and customer.birthdate.day == today.day
