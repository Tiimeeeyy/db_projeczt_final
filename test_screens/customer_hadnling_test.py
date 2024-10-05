import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QLineEdit, QStackedWidget
from customer_handling import CustomerHandling

class RegisterScreen(QWidget):
    def __init__(self, customer_handling):
        super().__init__()
        self.customer_handling = customer_handling
        layout = QVBoxLayout()

        self.label = QLabel("Register", self)
        layout.addWidget(self.label)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        layout.addWidget(self.name_input)

        self.gender_input = QLineEdit(self)
        self.gender_input.setPlaceholderText("Gender")
        layout.addWidget(self.gender_input)

        self.birthdate_input = QLineEdit(self)
        self.birthdate_input.setPlaceholderText("Birthdate (YYYY-MM-DD)")
        layout.addWidget(self.birthdate_input)

        self.address_input = QLineEdit(self)
        self.address_input.setPlaceholderText("Address")
        layout.addWidget(self.address_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register(self):
        name = self.name_input.text()
        gender = self.gender_input.text()
        birthdate = self.birthdate_input.text()
        address = self.address_input.text()
        password = self.password_input.text()
        self.customer_handling.register_customer(name, gender, birthdate, address, password)
        self.label.setText("Registration successful!")

class LoginScreen(QWidget):
    def __init__(self, customer_handling):
        super().__init__()
        self.customer_handling = customer_handling
        layout = QVBoxLayout()

        self.label = QLabel("Login", self)
        layout.addWidget(self.label)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Name")
        layout.addWidget(self.name_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        name = self.name_input.text()
        password = self.password_input.text()
        if self.customer_handling.login_customer(name, password):
            self.label.setText("Login successful!")
        else:
            self.label.setText("Invalid name or password.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Handling")
        self.setGeometry(100, 100, 400, 300)

        self.customer_handling = CustomerHandling('mysql+pymysql://root:hello@localhost/pizza')

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.register_screen = RegisterScreen(self.customer_handling)
        self.login_screen = LoginScreen(self.customer_handling)

        self.stacked_widget.addWidget(self.register_screen)
        self.stacked_widget.addWidget(self.login_screen)

        self.show_login_screen()
    def show_register_screen(self):
        self.stacked_widget.setCurrentWidget(self.register_screen)

    def show_login_screen(self):
        self.stacked_widget.setCurrentWidget(self.login_screen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())