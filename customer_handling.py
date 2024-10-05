from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Customer

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