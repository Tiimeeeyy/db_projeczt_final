import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from pizza_service import PizzaService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pizza Ordering System")
        self.setGeometry(100, 100, 600, 400)

        # Set up the layout
        layout = QVBoxLayout()

        # Add a label
        self.label = QLabel("Welcome to the Pizza Ordering System")
        layout.addWidget(self.label)

        # Add a button to fetch pizzas
        self.button = QPushButton("Fetch Pizzas")
        self.button.clicked.connect(self.fetch_pizzas)
        layout.addWidget(self.button)

        # Set the central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Set up the pizza service
        self.pizza_service = PizzaService('mysql+pymysql://root:hello@localhost/pizza')

    def fetch_pizzas(self):
        pizzas = self.pizza_service.fetch_pizzas()
        if not pizzas:
            self.label.setText("No pizzas found in the database.")
        else:
            pizza_names = [pizza.name for pizza in pizzas]
            self.label.setText("Pizzas: " + ", ".join(pizza_names))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())