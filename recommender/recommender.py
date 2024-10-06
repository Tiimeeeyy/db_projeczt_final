from sqlalchemy.orm import sessionmaker
from  sqlalchemy import create_engine
from models import Pizza, Ingredient, pizza_ingredients
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

class Recommender:
    def __init__(self, db_url):
        engine = create_engine(db_url)
        engine = sessionmaker(bind=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def fetch_pizzas_with_ingredient(self):
        try:
            pizzas = self.session.query(Pizza).all()
            for pizza in pizzas:
                ingredients =

        except Exception as e:
            print(f"Something went wrong {e}")