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
        if self.session:
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

    def register_customer(self, name, gender, birthdate, address, password):
        if not self.session:
            print("Database session is not available.")
            return False

        new_customer = Customer(
            name=name,
            gender=gender,
            birthdate=birthdate,
            address=address
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

        self.reg_confirm_password_entry = ctk.CTkEntry(self.register_frame, placeholder_text="Confirm Password", show="*")
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

        pizzas = self.pizza_handler.get_pizzas()
        for pizza in pizzas:
            pizza_label = ctk.CTkLabel(self.menu_frame, text=f"{pizza.name} - ${pizza.price}")
            pizza_label.pack(pady=(5, 5))

        logout_button = ctk.CTkButton(self.menu_frame, text="Logout", command=self.show_login_frame)
        logout_button.pack(pady=(10, 20))

    def init_admin_menu_frame(self):
        self.admin_menu_frame = ctk.CTkScrollableFrame(self, corner_radius=15)

        admin_menu_label = ctk.CTkLabel(self.admin_menu_frame, text="Admin Menu", font=ctk.CTkFont(size=24, weight="bold"))
        admin_menu_label.pack(pady=(10, 20))

        item_types = ["Pizza", "Drink", "Dessert"]
        selected_item_type = ctk.StringVar(value="Pizza")
        item_type_label = ctk.CTkLabel(self.admin_menu_frame, text="Select Item Type:")
        item_type_label.pack(pady=(10, 5))
        item_type_dropdown = ctk.CTkOptionMenu(self.admin_menu_frame, values=item_types, variable=selected_item_type, command=self.update_item_fields)
        item_type_dropdown.pack(pady=(5, 20))

        self.item_fields_frame = ctk.CTkFrame(self.admin_menu_frame)
        self.item_fields_frame.pack(pady=(5, 20), fill="both", expand=True)

        self.update_item_fields(selected_item_type.get())
        save_button = ctk.CTkButton(self.admin_menu_frame, text="Save", command=lambda: self.save_item(selected_item_type.get()))
        save_button.pack(pady=(10, 10))
        back_button = ctk.CTkButton(self.admin_menu_frame, text="Back", command=self.show_login_frame)
        back_button.pack(pady=(10, 10))

    def update_item_fields(self, item_type):
        for widget in self.item_fields_frame.winfo_children():
            widget.destroy()

        if item_type == "Pizza":
            self.name_entry = ctk.CTkEntry(self.item_fields_frame, placeholder_text="Pizza Name")
            self.name_entry.pack(pady=(10, 5))
            self.price_entry = ctk.CTkEntry(self.item_fields_frame, placeholder_text="Price")
            self.price_entry.pack(pady=(10, 5))
            self.is_vegetarian_var = ctk.BooleanVar()
            self.is_vegan_var = ctk.BooleanVar()
            vegetarian_checkbox = ctk.CTkCheckBox(self.item_fields_frame, text="Vegetarian", variable=self.is_vegetarian_var)
            vegetarian_checkbox.pack(pady=(10, 5))
            vegan_checkbox = ctk.CTkCheckBox(self.item_fields_frame, text="Vegan", variable=self.is_vegan_var)
            vegan_checkbox.pack(pady=(10, 5))

        elif item_type == "Drink":
            self.name_entry = ctk.CTkEntry(self.item_fields_frame, placeholder_text="Drink Name")
            self.name_entry.pack(pady=(10, 5))
            self.price_entry = ctk.CTkEntry(self.item_fields_frame, placeholder_text="Price")
            self.price_entry.pack(pady=(10, 5))

        elif item_type == "Dessert":
            self.name_entry = ctk.CTkEntry(self.item_fields_frame, placeholder_text="Dessert Name")
            self.name_entry.pack(pady=(10, 5))
            self.price_entry = ctk.CTkEntry(self.item_fields_frame, placeholder_text="Price")
            self.price_entry.pack(pady=(10, 5))

    def save_item(self, item_type):
        if item_type == "Pizza":
            name = self.name_entry.get()
            price = float(self.price_entry.get())
            is_vegetarian = self.is_vegetarian_var.get()
            is_vegan = self.is_vegan_var.get()
            self.pizza_handler.add_pizza(name, price, is_vegetarian, is_vegan)

        elif item_type in ["Drink", "Dessert"]:
            name = self.name_entry.get()
            price = float(self.price_entry.get())
            self.pizza_handler.add_pizza(name, price, is_vegetarian=False, is_vegan=False)

        self.admin_menu_frame.pack_forget()
        self.admin_menu_frame.destroy()
        self.init_admin_menu_frame()
        self.admin_menu_frame.pack(pady=50, padx=50, fill="both", expand=True)

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

    def login_customer(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        login_result = self.customer_handler.login_customer(username, password)
        if login_result == "customer":
            self.login_frame.pack_forget()
            self.login_frame.destroy()
            self.init_menu_frame()
            self.menu_frame.pack(pady=50, padx=50, fill="both", expand=True)
        else:
            error_label = ctk.CTkLabel(self.login_frame, text="Login failed! Invalid credentials.", text_color="white", fg_color="red", corner_radius=10)
            error_label.pack(pady=(5, 10))
            self.after(1000, error_label.destroy)

    def login_admin(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.customer_handler.login_admin(username, password):
            self.login_frame.pack_forget()
            self.login_frame.destroy()
            self.init_admin_menu_frame()
            self.admin_menu_frame.pack(pady=50, padx=50, fill="both", expand=True)
        else:
            error_label = ctk.CTkLabel(self.login_frame, text="Admin login failed! Invalid credentials.", text_color="white", fg_color="red", corner_radius=10)
            error_label.pack(pady=(5, 10))
            self.after(1000, error_label.destroy)

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
                self.show_login_frame()
                print("Registered successfully! Please log in.")
        else:
            print("Passwords do not match.")


if __name__ == "__main__":
    app = PizzaGUI()
    app.mainloop()