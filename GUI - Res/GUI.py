import customtkinter as ctk
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from models import Customer, Pizza, Admin

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


class CustomerHandling:
    def __init__(self, db_url):
        try:
            engine = create_engine(db_url)
            session = sessionmaker(bind=engine)
            self.session = session()
            self.create_default_admin()
        except exc.SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")
            self.session = None

    def create_default_admin(self):
        admin = self.session.query(Admin).filter_by(name="admin").first()
        if not admin:
            new_admin = Admin(name="admin", gender="N/A", password="")
            new_admin.set_pw("admin123")
            try:
                self.session.add(new_admin)
                self.session.commit()
                print("Default admin created with username 'admin' and password 'admin123'.")
            except Exception as e:
                self.session.rollback()
                print(f"Error creating default admin: {e}")

    def register_customer(self, name, gender, birthdate, address, password, is_admin=False):
        if not self.session:
            print("Database session is not available.")
            return False

        new_customer = Customer(
            name=name,
            gender=gender,
            birthdate=birthdate,
            address=address,
            is_admin=is_admin
        )
        new_customer.set_pw(password)
        try:
            self.session.add(new_customer)
            self.session.commit()
            print(f"Customer '{name}' registered successfully")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error registering customer: {e}")
            return False

    def login_customer(self, username, password):
        if not self.session:
            print("Database session is not available.")
            return False

        customer = self.session.query(Customer).filter_by(name=username).first()
        if customer and customer.check_pw(password):
            if customer.is_admin:
                print(f"Admin '{username}' logged in successfully")
                return "admin"
            else:
                print(f"Customer '{username}' logged in successfully")
                return "customer"
        else:
            print("Invalid username or password")
            return False

    def login_admin(self, username, password):
        if not self.session:
            print("Database session is not available.")
            return False

        admin = self.session.query(Admin).filter_by(name=username).first()
        if admin and admin.check_pw(password):
            print(f"Admin '{username}' logged in successfully")
            return True
        else:
            print("Invalid admin username or password")
            return False


class PizzaHandling:
    def __init__(self, db_url):
        try:
            engine = create_engine(db_url)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        except exc.SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")
            self.session = None

    def get_pizzas(self):
        if not self.session:
            print("Database session is not available.")
            return []

        try:
            pizzas = self.session.query(Pizza).all()
            return pizzas
        except exc.SQLAlchemyError as e:
            print(f"Error retrieving pizzas: {e}")
            return []

    def add_pizza(self, name, price, is_vegetarian, is_vegan):
        if not self.session:
            print("Database session is not available.")
            return False

        new_pizza = Pizza(name=name, price=price, is_vegetarian=is_vegetarian, is_vegan=is_vegan)
        self.session.add(new_pizza)
        try:
            self.session.commit()
            print(f"Pizza '{name}' added to the catalogue.")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error adding pizza: {e}")
            return False


class PizzaGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.customer_handler = CustomerHandling("mysql+pymysql://root:Porto123@localhost/pizza_db")
        self.pizza_handler = PizzaHandling("mysql+pymysql://root:Porto123@localhost/pizza_db")

        self.title("1453-Pizza")
        self.geometry("500x600")
        self.resizable(False, False)

        self.init_login_frame()
        self.login_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def init_login_frame(self):
        self.login_frame = ctk.CTkFrame(self, corner_radius=15)

        screen_label = ctk.CTkLabel(self.login_frame, text="1453-Pizza", font=ctk.CTkFont(size=24, weight="bold"))
        screen_label.pack(pady=(10, 20))

        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username")
        self.username_entry.pack(pady=10, fill="x")

        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10, fill="x")

        login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login_customer)
        login_button.pack(pady=(10, 20))

        admin_login_button = ctk.CTkButton(self.login_frame, text="Admin Login", command=self.login_admin)
        admin_login_button.pack(pady=(10, 20))

        register_label = ctk.CTkLabel(self.login_frame, text="Don't have an account?")
        register_label.pack()

        switch_to_register = ctk.CTkButton(self.login_frame, text="Register", command=self.show_register_frame)
        switch_to_register.pack(pady=(5, 10))

    def init_register_frame(self):
        self.register_frame = ctk.CTkScrollableFrame(self, corner_radius=15, width=450, height=550)

        register_label = ctk.CTkLabel(self.register_frame, text="Register", font=ctk.CTkFont(size=24, weight="bold"))
        register_label.pack(pady=(10, 20))

        self.reg_username_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Username")
        self.reg_username_entry.pack(pady=10, fill="x")

        self.reg_password_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Password", show="*")
        self.reg_password_entry.pack(pady=10, fill="x")

        self.reg_confirm_password_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Confirm Password",
                                                       show="*")
        self.reg_confirm_password_entry.pack(pady=10, fill="x")

        self.reg_gender_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Gender")
        self.reg_gender_entry.pack(pady=10, fill="x")

        self.reg_birthdate_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Birthdate (YYYY-MM-DD)")
        self.reg_birthdate_entry.pack(pady=10, fill="x")

        self.reg_address_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Address")
        self.reg_address_entry.pack(pady=10, fill="x")

        register_button = ctk.CTkButton(self.register_frame, text="Register", command=self.register_customer)
        register_button.pack(pady=(10, 20))

        login_label = ctk.CTkLabel(self.register_frame, text="Already have an account?")
        login_label.pack()

        switch_to_login = ctk.CTkButton(self.register_frame, text="Login", command=self.show_login_frame)
        switch_to_login.pack(pady=(5, 10))

    def init_menu_frame(self):
        self.menu_frame = ctk.CTkScrollableFrame(self, corner_radius=15)

        menu_label = ctk.CTkLabel(self.menu_frame, text="Main Menu", font=ctk.CTkFont(size=24, weight="bold"))
        menu_label.pack(pady=(10, 20))

        logout_button = ctk.CTkButton(self.menu_frame, text="Logout", command=self.show_login_frame)
        logout_button.pack(pady=(10, 20))

    def init_admin_menu_frame(self):
        self.admin_menu_frame = ctk.CTkScrollableFrame(self, corner_radius=15)

        admin_menu_label = ctk.CTkLabel(self.admin_menu_frame, text="Admin Menu", font=ctk.CTkFont(size=24, weight="bold"))
        admin_menu_label.pack(pady=(10, 20))

        add_pizza_button = ctk.CTkButton(self.admin_menu_frame, text="Add Pizza", command=self.admin_add_pizza)
        add_pizza_button.pack(pady=(10, 10))

        logout_button = ctk.CTkButton(self.admin_menu_frame, text="Logout", command=self.show_login_frame)
        logout_button.pack(pady=(10, 20))

    def show_login_frame(self):
        if hasattr(self, 'register_frame') and self.register_frame is not None:
            self.register_frame.pack_forget()
            self.register_frame.destroy()
        if hasattr(self, 'menu_frame') and self.menu_frame is not None:
            self.menu_frame.pack_forget()
            self.menu_frame.destroy()
        if hasattr(self, 'admin_menu_frame') and self.admin_menu_frame is not None:
            self.admin_menu_frame.pack_forget()
            self.admin_menu_frame.destroy()
        self.init_login_frame()
        self.login_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def show_register_frame(self):
        if hasattr(self, 'login_frame') and self.login_frame is not None:
            self.login_frame.pack_forget()
            self.login_frame.destroy()
        self.init_register_frame()
        self.register_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def show_menu_frame(self, is_admin=False):
        if hasattr(self, 'login_frame') and self.login_frame is not None:
            self.login_frame.pack_forget()
            self.login_frame.destroy()
        if is_admin:
            self.init_admin_menu_frame()
            self.admin_menu_frame.pack(pady=50, padx=50, fill="both", expand=True)
        else:
            self.init_menu_frame()
            pizzas = self.pizza_handler.get_pizzas()

            for widget in self.menu_frame.winfo_children():
                widget.destroy()

            if not pizzas:
                no_pizza_label = ctk.CTkLabel(self.menu_frame, text="No pizzas available.")
                no_pizza_label.pack(pady=(5, 5), padx=(5, 5), fill="x")
            else:
                for pizza in pizzas:
                    pizza_label = ctk.CTkLabel(self.menu_frame, text=f"{pizza.name} - {pizza.price}e")
                    pizza_label.pack(pady=(5, 5), padx=(5, 5), fill="x")

                    addtocart_button = ctk.CTkButton(self.menu_frame, text="Add",
                                                     command=lambda p=pizza: self.order_pizza(p))
                    addtocart_button.pack(pady=(5, 5), padx=(5, 5), fill="x")

            self.menu_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def order_pizza(self, pizza):
        if not hasattr(self, 'order_cart'):
            self.order_cart = []

        self.order_cart.append(pizza)
        self.show_message(f"{pizza.name} added to cart.", bg_color="green", text_color="white")

        for item in self.order_cart:
            print(f"Cart: {item.name} - {item.price}e")

    def checkout_order(self):
        if not hasattr(self, 'order_cart') or len(self.order_cart) == 0:
            self.show_message("Your cart is empty!", bg_color="red", text_color="white")
            return

        total_price = sum([pizza.price for pizza in self.order_cart])
        self.show_message(f"Order placed! Total: {total_price}e", bg_color="green", text_color="white")

        self.order_cart = []
        print("Order checkout completed.")

    def register_customer(self):
        name = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_password_entry.get()
        gender = self.reg_gender_entry.get()
        birthdate = self.reg_birthdate_entry.get()
        address = self.reg_address_entry.get()

        if password == confirm_password:
            success = self.customer_handler.register_customer(name, gender, birthdate, address, password)
            if success:
                self.register_frame.pack_forget()
                self.register_frame.destroy()
                self.init_login_frame()
                self.login_frame.pack(pady=50, padx=50, fill="both", expand=True)
                self.show_message("Registered successfully! Please log in.", bg_color="green", text_color="white")
        else:
            self.show_message("Passwords do not match.", bg_color="red", text_color="white")

    def login_customer(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        login_result = self.customer_handler.login_customer(username, password)
        if login_result == "admin":
            self.show_menu_frame(is_admin=True)
        elif login_result == "customer":
            self.show_menu_frame()
        else:
            self.show_message("Login failed!", bg_color="red", text_color="white")

    def login_admin(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.customer_handler.login_admin(username, password):
            self.show_menu_frame(is_admin=True)
        else:
            self.show_message("Admin login failed!", bg_color="red", text_color="white")

    def admin_add_pizza(self):



    def show_message(self, message, bg_color="green", text_color="white"):
        message_label = ctk.CTkLabel(self, text=message, font=ctk.CTkFont(size=14), fg_color=bg_color,
                                     text_color=text_color, corner_radius=15)
        message_label.pack(pady=(10, 10), padx=(10, 10), fill="x")
        self.after(1500, message_label.destroy)


if __name__ == "__main__":
    app = PizzaGUI()
    app.mainloop()