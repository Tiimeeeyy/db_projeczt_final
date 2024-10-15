import customtkinter as ctk
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from models import Customer, Pizza, Drink, Dessert, Admin

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


class ItemHandling:
    def __init__(self, db_url):
        try:
            engine = create_engine(db_url)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        except exc.SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")
            self.session = None

    def get_items(self, item_type):
        if not self.session:
            print("Database session is not available.")
            return []

        try:
            if item_type == "Pizza":
                items = self.session.query(Pizza).all()
            elif item_type == "Drink":
                items = self.session.query(Drink).all()
            elif item_type == "Dessert":
                items = self.session.query(Dessert).all()
            else:
                items = []
            return items
        except exc.SQLAlchemyError as e:
            print(f"Error retrieving items: {e}")
            return []

    def add_item(self, item_type, name, price, **kwargs):
        if not self.session:
            print("Database session is not available.")
            return False

        if item_type == "Pizza":
            new_item = Pizza(name=name, price=price, is_vegetarian=kwargs.get("is_vegetarian", False),
                             is_vegan=kwargs.get("is_vegan", False))
        elif item_type == "Drink":
            new_item = Drink(name=name, price=price)
        elif item_type == "Dessert":
            new_item = Dessert(name=name, price=price)
        else:
            print(f"Invalid item type: {item_type}")
            return False

        self.session.add(new_item)
        try:
            self.session.commit()
            print(f"{item_type} '{name}' added to the catalogue.")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error adding {item_type.lower()}: {e}")
            return False

    def update_item(self, item_type, item_id, name=None, price=None, **kwargs):
        if not self.session:
            print("Database session is not available.")
            return False

        try:
            if item_type == "Pizza":
                item = self.session.query(Pizza).get(item_id)
                if name:
                    item.name = name
                if price is not None:
                    item.price = price
                if "is_vegetarian" in kwargs:
                    item.is_vegetarian = kwargs["is_vegetarian"]
                if "is_vegan" in kwargs:
                    item.is_vegan = kwargs["is_vegan"]
            elif item_type == "Drink":
                item = self.session.query(Drink).get(item_id)
                if name:
                    item.name = name
                if price is not None:
                    item.price = price
            elif item_type == "Dessert":
                item = self.session.query(Dessert).get(item_id)
                if name:
                    item.name = name
                if price is not None:
                    item.price = price
            else:
                print(f"Invalid item type: {item_type}")
                return False

            self.session.commit()
            print(f"{item_type} '{item.name}' updated successfully.")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error updating {item_type.lower()}: {e}")
            return False


class ItemGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.customer_handler = CustomerHandling("mysql+pymysql://root:Porto123@localhost/pizza_db")
        self.item_handler = ItemHandling("mysql+pymysql://root:Porto123@localhost/pizza_db")

        self.title("1453-Items")
        self.geometry("500x600")
        self.resizable(False, False)

        self.init_login_frame()
        self.login_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def init_login_frame(self):
        self.login_frame = ctk.CTkFrame(self, corner_radius=15)

        screen_label = ctk.CTkLabel(self.login_frame, text="1453-Items", font=ctk.CTkFont(size=24, weight="bold"))
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

        item_types = ["Pizza", "Drink", "Dessert"]
        for item_type in item_types:
            items = self.item_handler.get_items(item_type)
            for item in items:
                item_label = ctk.CTkLabel(self.menu_frame, text=f"{item.name} - ${item.price}")
                item_label.pack(pady=(5, 5))

        logout_button = ctk.CTkButton(self.menu_frame, text="Logout", command=self.show_login_frame)
        logout_button.pack(pady=(10, 20))

    def init_admin_menu_frame(self):
        self.admin_menu_frame = ctk.CTkScrollableFrame(self, corner_radius=15)

        admin_menu_label = ctk.CTkLabel(self.admin_menu_frame, text="Admin Menu",
                                        font=ctk.CTkFont(size=24, weight="bold"))
        admin_menu_label.pack(pady=(10, 20))

        add_item_button = ctk.CTkButton(self.admin_menu_frame, text="Add Item", command=self.show_add_item_frame)
        add_item_button.pack(pady=(10, 10))

        update_item_button = ctk.CTkButton(self.admin_menu_frame, text="Update Item",
                                           command=self.show_update_item_frame)
        update_item_button.pack(pady=(10, 10))

        back_button = ctk.CTkButton(self.admin_menu_frame, text="Back", command=self.show_login_frame)
        back_button.pack(pady=(10, 10))

    def show_add_item_frame(self):
        if hasattr(self, 'admin_menu_frame') and self.admin_menu_frame is not None:
            self.admin_menu_frame.pack_forget()
            self.admin_menu_frame.destroy()
        self.init_add_item_frame()
        self.add_item_frame.pack(pady=50, padx=50, fill="both", expand=True)
        if hasattr(self, 'add_item_frame') and self.add_item_frame is not None:
            self.add_item_frame.destroy()
        self.init_add_item_frame()
        self.add_item_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def show_update_item_frame(self):
        if hasattr(self, 'admin_menu_frame') and self.admin_menu_frame is not None:
            self.admin_menu_frame.pack_forget()
            self.admin_menu_frame.destroy()
        self.init_update_item_frame()
        self.update_item_frame.pack(pady=50, padx=50, fill="both", expand=True)
        if hasattr(self, 'update_item_frame') and self.update_item_frame is not None:
            self.update_item_frame.destroy()
        self.init_update_item_frame()
        self.update_item_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def init_add_item_frame(self):
        self.add_item_frame = ctk.CTkScrollableFrame(self, corner_radius=15)

        item_types = ["Pizza", "Drink", "Dessert"]
        selected_item_type = ctk.StringVar(value="Pizza")
        item_type_label = ctk.CTkLabel(self.add_item_frame, text="Select Item Type:")
        item_type_label.pack(pady=(10, 5))
        item_type_dropdown = ctk.CTkOptionMenu(self.add_item_frame, values=item_types, variable=selected_item_type,
                                               command=self.update_add_item_fields)
        item_type_dropdown.pack(pady=(5, 20))

        self.add_item_fields_frame = ctk.CTkFrame(self.add_item_frame)
        self.add_item_fields_frame.pack(pady=(5, 20), fill="both", expand=True)

        self.update_add_item_fields(selected_item_type.get())
        save_button = ctk.CTkButton(self.add_item_frame, text="Save",
                                    command=lambda: self.save_item(selected_item_type.get()))
        save_button.pack(pady=(10, 10))
        back_button = ctk.CTkButton(self.add_item_frame, text="Back", command=self.show_admin_menu_frame)
        back_button.pack(pady=(10, 10))

    def init_update_item_frame(self):
        self.update_item_frame = ctk.CTkScrollableFrame(self, corner_radius=15)

        item_types = ["Pizza", "Drink", "Dessert"]
        selected_item_type = ctk.StringVar(value="Pizza")
        item_type_label = ctk.CTkLabel(self.update_item_frame, text="Select Item Type:")
        item_type_label.pack(pady=(10, 5))
        item_type_dropdown = ctk.CTkOptionMenu(self.update_item_frame, values=item_types, variable=selected_item_type,
                                               command=self.update_update_item_fields)
        item_type_dropdown.pack(pady=(5, 20))

        self.update_item_fields_frame = ctk.CTkFrame(self.update_item_frame)
        self.update_item_fields_frame.pack(pady=(5, 20), fill="both", expand=True)

        self.update_update_item_fields(selected_item_type.get())
        update_button = ctk.CTkButton(self.update_item_frame, text="Update",
                                      command=lambda: self.update_item(selected_item_type.get()))
        update_button.pack(pady=(10, 10))
        back_button = ctk.CTkButton(self.update_item_frame, text="Back", command=self.show_admin_menu_frame)
        back_button.pack(pady=(10, 10))

    def update_add_item_fields(self, item_type):
        for widget in self.add_item_fields_frame.winfo_children():
            widget.destroy()

        if item_type == "Pizza":
            self.name_entry = ctk.CTkEntry(self.add_item_fields_frame, placeholder_text="Pizza Name")
            self.name_entry.pack(pady=(10, 5))
            self.price_entry = ctk.CTkEntry(self.add_item_fields_frame, placeholder_text="Price")
            self.price_entry.pack(pady=(10, 5))
            self.is_vegetarian_var = ctk.BooleanVar()
            self.is_vegan_var = ctk.BooleanVar()
            vegetarian_checkbox = ctk.CTkCheckBox(self.add_item_fields_frame, text="Vegetarian",
                                                  variable=self.is_vegetarian_var)
            vegetarian_checkbox.pack(pady=(10, 5))
            vegan_checkbox = ctk.CTkCheckBox(self.add_item_fields_frame, text="Vegan", variable=self.is_vegan_var)
            vegan_checkbox.pack(pady=(10, 5))

        elif item_type == "Drink":
            self.name_entry = ctk.CTkEntry(self.add_item_fields_frame, placeholder_text="Drink Name")
            self.name_entry.pack(pady=(10, 5))
            self.price_entry = ctk.CTkEntry(self.add_item_fields_frame, placeholder_text="Price")
            self.price_entry.pack(pady=(10, 5))

        elif item_type == "Dessert":
            self.name_entry = ctk.CTkEntry(self.add_item_fields_frame, placeholder_text="Dessert Name")
            self.name_entry.pack(pady=(10, 5))
            self.price_entry = ctk.CTkEntry(self.add_item_fields_frame, placeholder_text="Price")
            self.price_entry.pack(pady=(10, 5))

    def update_update_item_fields(self, item_type):
        for widget in self.update_item_fields_frame.winfo_children():
            widget.destroy()

        self.item_id_entry = ctk.CTkEntry(self.update_item_fields_frame, placeholder_text="Item ID")
        self.item_id_entry.pack(pady=(10, 5))

        if item_type == "Pizza":
            self.name_entry = ctk.CTkEntry(self.update_item_fields_frame, placeholder_text="Pizza Name")
            self.name_entry.pack(pady=(10, 5))
            self.price_entry = ctk.CTkEntry(self.update_item_fields_frame, placeholder_text="Price")
            self.price_entry.pack(pady=(10, 5))
            self.is_vegetarian_var = ctk.BooleanVar()
            self.is_vegan_var = ctk.BooleanVar()
            vegetarian_checkbox = ctk.CTkCheckBox(self.update_item_fields_frame, text="Vegetarian",
                                                  variable=self.is_vegetarian_var)
            vegetarian_checkbox.pack(pady=(10, 5))
            vegan_checkbox = ctk.CTkCheckBox(self.update_item_fields_frame, text="Vegan", variable=self.is_vegan_var)
            vegan_checkbox.pack(pady=(10, 5))

        elif item_type == "Drink":
            self.name_entry = ctk.CTkEntry(self.update_item_fields_frame, placeholder_text="Drink Name")
            self.name_entry.pack(pady=(10, 5))
            self.price_entry = ctk.CTkEntry(self.update_item_fields_frame, placeholder_text="Price")
            self.price_entry.pack(pady=(10, 5))

        elif item_type == "Dessert":
            self.name_entry = ctk.CTkEntry(self.update_item_fields_frame, placeholder_text="Dessert Name")
            self.name_entry.pack(pady=(10, 5))
            self.price_entry = ctk.CTkEntry(self.update_item_fields_frame, placeholder_text="Price")
            self.price_entry.pack(pady=(10, 5))

    def save_item(self, item_type):
        if hasattr(self, 'add_item_fields_frame') and self.add_item_fields_frame is not None:
            for widget in self.add_item_fields_frame.winfo_children():
                widget.destroy()
        name = self.name_entry.get()
        price = float(self.price_entry.get())
        if item_type == "Pizza":
            is_vegetarian = self.is_vegetarian_var.get()
            is_vegan = self.is_vegan_var.get()
            self.item_handler.add_item(item_type, name, price, is_vegetarian=is_vegetarian, is_vegan=is_vegan)
        else:
            self.item_handler.add_item(item_type, name, price)

        self.init_admin_menu_frame()
        self.admin_menu_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def update_item(self, item_type):
        if hasattr(self, 'update_item_fields_frame') and self.update_item_fields_frame is not None:
            for widget in self.update_item_fields_frame.winfo_children():
                widget.destroy()
        item_id = int(self.item_id_entry.get())
        name = self.name_entry.get()
        price = float(self.price_entry.get()) if self.price_entry.get() else None
        if item_type == "Pizza":
            is_vegetarian = self.is_vegetarian_var.get()
            is_vegan = self.is_vegan_var.get()
            self.item_handler.update_item(item_type, item_id, name, price, is_vegetarian=is_vegetarian,
                                          is_vegan=is_vegan)
        else:
            self.item_handler.update_item(item_type, item_id, name, price)

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
            error_label = ctk.CTkLabel(self.login_frame, text="Login failed! Invalid credentials.", text_color="white",
                                       fg_color="red", corner_radius=10)
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
            error_label = ctk.CTkLabel(self.login_frame, text="Admin login failed! Invalid credentials.",
                                       text_color="white", fg_color="red", corner_radius=10)
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
    app = ItemGUI()
    app.mainloop()