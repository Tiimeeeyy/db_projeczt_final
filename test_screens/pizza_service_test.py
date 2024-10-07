import logging
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QTextEdit
from pizza_service import PizzaService
# TEST GUI for testing functionalities
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
class TestGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pizza Service Test GUI")
        self.setGeometry(100, 100, 600, 400)

        # Set up the layout
        layout = QVBoxLayout()

        # Add a label to display messages
        self.label = QLabel("Test the Pizza Service functionality", self)
        layout.addWidget(self.label)

        # Add a text edit to display fetched pizzas
        self.pizza_display = QTextEdit(self)
        self.pizza_display.setReadOnly(True)
        layout.addWidget(self.pizza_display)

        # Add buttons to test different functionalities
        self.add_pizza_button = QPushButton("Add Pizza", self)
        self.add_pizza_button.clicked.connect(self.add_pizza)
        layout.addWidget(self.add_pizza_button)

        self.fetch_pizzas_button = QPushButton("Fetch Pizzas", self)
        self.fetch_pizzas_button.clicked.connect(self.fetch_pizzas)
        layout.addWidget(self.fetch_pizzas_button)

        self.update_pizza_button = QPushButton("Update Pizza", self)
        self.update_pizza_button.clicked.connect(self.update_pizza)
        layout.addWidget(self.update_pizza_button)

        self.delete_pizza_button = QPushButton("Delete Pizza", self)
        self.delete_pizza_button.clicked.connect(self.delete_pizza)
        layout.addWidget(self.delete_pizza_button)

        # Set the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set up the pizza service
        self.pizza_service = PizzaService('mysql+pymysql://root:hello@localhost/pizza_db_new')

    def add_pizza(self):
        try:
            logging.debug("Adding Margharita Pizza")
            self.pizza_service.add_pizza("Margherita", True, False, 8.99)
            self.label.setText("Added Margherita pizza.")
        except Exception as e:
            logging.error(f"An error occured {e}")
            self.label.setText(f"An error occured")

    def fetch_pizzas(self):
        try:
            logging.debug("Fetching pizzas from DB")
            pizzas = self.pizza_service.fetch_pizzas()
            logging.debug(f"Fetched {len(pizzas)} pizzas")
            if not pizzas:
                self.label.setText("No pizzas found in the database.")
            else:
                max_display = 100
                pizza_names = [pizza.name for pizza in pizzas[:max_display]]
                self.pizza_display.setText("\n".join(pizza_names))
                if len(pizzas) > max_display:
                    self.label.setText(f"Displaying first {max_display} pizzas out of {len(pizzas)} found.")
        except Exception as e:
            logging.error(f"An error occurred while fetching the pizzas: {e}")
            self.label.setText(f"An error occurred: {e}")

    def update_pizza(self):
        pizzas = self.pizza_service.fetch_pizzas()
        if pizzas:
            pizza = pizzas[0]
            self.pizza_service.update_pizza(pizza.Id, name="Pepperoni", is_vegetarian=False)
            self.label.setText(f"Updated pizza {pizza.Name} to Pepperoni.")
        else:
            self.label.setText("No pizzas to update.")

    def delete_pizza(self):
        try:
            logging.debug("Fetching pizzas for deletion")
            pizzas = self.pizza_service.fetch_pizzas()
            logging.debug(f"Fetched {len(pizzas)}")
            if pizzas:
                pizza = pizzas[0]
                logging.debug(f"Deleting pizza with ID {pizza.Id}")
                self.pizza_service.delete_pizza(pizza.Id)
                self.label.setText(f"Deleted pizza {pizza.name}.")
            else:
                self.label.setText("No pizzas to delete.")
        except Exception as e:
            logging.error(f"An error occurred while deleting pizza: {e}")
            self.label.setText(f"An error occurred: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestGUI()
    window.show()
    sys.exit(app.exec_())