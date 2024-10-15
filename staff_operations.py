from datetime import datetime

from sqlalchemy import create_engine, func, extract
from sqlalchemy.orm import sessionmaker

from models import Order


class StaffOp:
	def __init__(self, db_url):
		engine = create_engine(db_url)
		session = sessionmaker(bind=engine)
		self.session = session()

	def display_pending_orders(self):
		try:
			pending_orders = (
				self.session.query(Order)
				.filter(Order.status != "Delivered")
				.order_by(Order.status)
				.all()
			)
			return pending_orders
		except Exception as e:
			print(f"An error occurred while displaying pending orders: {e}")
			return []

	def generate_monthly_earnings_report(self, postal_code_prefix=None):

		try:

			current_month = datetime.now().month
			current_year = datetime.now().year
			query = self.session.query(func.sum(Order.total_price)) \
				.filter(extract("month", Order.order_date) == current_month) \
				.filter(extract("year", Order.order_date) == current_year)

			if postal_code_prefix:
				query = query.filter(Order.postal_code.like(f"{postal_code_prefix}%"))

			monthly_earnings = query.scalar
			return monthly_earnings if monthly_earnings else 0.0

		except Exception as e:
			print(f"An error occurred while generating monthly earnings report: {e}")
			return 0.0