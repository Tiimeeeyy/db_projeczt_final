import customtkinter as ctk
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from models import Customer, Pizza, Drink, Dessert, Admin, Order
from datetime import datetime
import bcrypt

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


class CustomerHandling:
    def __init__(self, db_url):
        try:
            engine = create_engine(db_url)
            Session = sessionmaker(bind=engine)
            self.session = Session()
            self.create_default_admin()
        except exc.SQLAlchemyError as e:
            print(f"Error connecting to the database: {e}")
            self.session = None

    def create_default_admin(self):
        if self.session:
            admin = self.session.query(Admin).filter_by(name="admin").first()
            if not admin:
                new_admin = Admin(name="admin", gender="N/A")
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

        existing_customer = self.session.query(Customer).filter_by(name=name).first()
        if existing_customer:
            print(f"Customer '{name}' already exists.")
            return False

        try:
            birthdate_obj = datetime.strptime(birthdate, "%Y-%m-%d")
        except ValueError:
            print("Invalid birthdate format. Please use YYYY-MM-DD.")
            return False

        new_customer = Customer(
            name=name,
            gender=gender,
            birthdate=birthdate_obj,
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
            return "customer", customer.Id  # Return customer Id
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
            new_item = Pizza(
                name=name,
                price=price,
                is_vegetarian=kwargs.get("is_vegetarian", False),
                is_vegan=kwargs.get("is_vegan", False)
            )
        elif item_type == "Drink":
            new_item = Drink(
                name=name,
                price=price
            )
        elif item_type == "Dessert":
            new_item = Dessert(
                name=name,
                price=price
            )
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
                item = self.session.query(Pizza).filter_by(Id=item_id).first()
                if not item:
                    print(f"Pizza with ID {item_id} does not exist.")
                    return False
                if name:
                    item.name = name
                if price is not None:
                    item.price = price
                if "is_vegetarian" in kwargs:
                    item.is_vegetarian = kwargs["is_vegetarian"]
                if "is_vegan" in kwargs:
                    item.is_vegan = kwargs["is_vegan"]
            elif item_type == "Drink":
                item = self.session.query(Drink).filter_by(Id=item_id).first()
                if not item:
                    print(f"Drink with ID {item_id} does not exist.")
                    return False
                if name:
                    item.name = name
                if price is not None:
                    item.price = price
            elif item_type == "Dessert":
                item = self.session.query(Dessert).filter_by(Id=item_id).first()
                if not item:
                    print(f"Dessert with ID {item_id} does not exist.")
                    return False
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

    def delete_item(self, item_type, item_id):
        if not self.session:
            print("Database session is not available.")
            return False

        try:
            if item_type == "Pizza":
                item = self.session.query(Pizza).filter_by(Id=item_id).first()
            elif item_type == "Drink":
                item = self.session.query(Drink).filter_by(Id=item_id).first()
            elif item_type == "Dessert":
                item = self.session.query(Dessert).filter_by(Id=item_id).first()
            else:
                print(f"Invalid item type: {item_type}")
                return False

            if not item:
                print(f"{item_type} with ID {item_id} does not exist.")
                return False

            self.session.delete(item)
            self.session.commit()
            print(f"{item_type} with ID {item_id} deleted successfully.")
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error deleting {item_type.lower()}: {e}")
            return False


class ItemGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.customer_handler = CustomerHandling("mysql+pymysql://root:Porto123@localhost/pizza_db")
        self.item_handler = ItemHandling("mysql+pymysql://root:Porto123@localhost/pizza_db")

        self.title("1453-Items")
        self.geometry("500x600")
        self.resizable(False, False)

        self.current_frame = None
        self.current_user_id = None  # To keep track of the logged-in customer
        self.cart = []  # To store items added to cart

        self.show_login_frame()

    def clear_frame(self):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
            self.current_frame.destroy()

    def show_login_frame(self):
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self, corner_radius=15)
        self.current_frame.pack(pady=50, padx=50, fill="both", expand=True)

        screen_label = ctk.CTkLabel(self.current_frame, text="1453-Items", font=ctk.CTkFont(size=24, weight="bold"))
        screen_label.pack(pady=(10, 20))

        self.username_entry = ctk.CTkEntry(self.current_frame, placeholder_text="Username")
        self.username_entry.pack(pady=10, fill="x")

        self.password_entry = ctk.CTkEntry(self.current_frame, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10, fill="x")

        login_button = ctk.CTkButton(self.current_frame, text="Login", command=self.login_customer)
        login_button.pack(pady=(10, 10))

        admin_login_button = ctk.CTkButton(self.current_frame, text="Admin Login", command=self.login_admin)
        admin_login_button.pack(pady=(0, 20))

        register_label = ctk.CTkLabel(self.current_frame, text="Don't have an account?")
        register_label.pack()

        switch_to_register = ctk.CTkButton(self.current_frame, text="Register", command=self.show_register_frame)
        switch_to_register.pack(pady=(5, 10))

    def show_register_frame(self):
        self.clear_frame()
        self.current_frame = ctk.CTkScrollableFrame(self, corner_radius=15, width=450, height=550)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

        register_label = ctk.CTkLabel(self.current_frame, text="Register", font=ctk.CTkFont(size=24, weight="bold"))
        register_label.pack(pady=(10, 20))

        self.reg_username_entry = ctk.CTkEntry(self.current_frame, placeholder_text="Username")
        self.reg_username_entry.pack(pady=10, fill="x")

        self.reg_password_entry = ctk.CTkEntry(self.current_frame, placeholder_text="Password", show="*")
        self.reg_password_entry.pack(pady=10, fill="x")

        self.reg_confirm_password_entry = ctk.CTkEntry(self.current_frame, placeholder_text="Confirm Password",
                                                       show="*")
        self.reg_confirm_password_entry.pack(pady=10, fill="x")

        self.reg_gender_entry = ctk.CTkEntry(self.current_frame, placeholder_text="Gender")
        self.reg_gender_entry.pack(pady=10, fill="x")

        self.reg_birthdate_entry = ctk.CTkEntry(self.current_frame, placeholder_text="Birthdate (YYYY-MM-DD)")
        self.reg_birthdate_entry.pack(pady=10, fill="x")

        self.reg_address_entry = ctk.CTkEntry(self.current_frame, placeholder_text="Address")
        self.reg_address_entry.pack(pady=10, fill="x")

        register_button = ctk.CTkButton(self.current_frame, text="Register", command=self.register_customer)
        register_button.pack(pady=(10, 20))

        login_label = ctk.CTkLabel(self.current_frame, text="Already have an account?")
        login_label.pack()

        switch_to_login = ctk.CTkButton(self.current_frame, text="Login", command=self.show_login_frame)
        switch_to_login.pack(pady=(5, 10))

    def show_menu_frame(self):
        self.clear_frame()
        self.current_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

        menu_label = ctk.CTkLabel(self.current_frame, text="Menu", font=ctk.CTkFont(size=24, weight="bold"))
        menu_label.pack(pady=(10, 20))

        item_types = ["Pizza", "Drink", "Dessert"]
        for item_type in item_types:
            items = self.item_handler.get_items(item_type)
            if items:
                section_label = ctk.CTkLabel(self.current_frame, text=item_type,
                                             font=ctk.CTkFont(size=20, weight="bold"))
                section_label.pack(pady=(10, 5))
                for item in items:
                    item_frame = ctk.CTkFrame(self.current_frame)
                    item_frame.pack(pady=(2, 2), fill="x")

                    item_label = ctk.CTkLabel(item_frame, text=f"{item.name} - ${item.price}")
                    item_label.pack(side="left")

                    add_button = ctk.CTkButton(item_frame, text="Add",
                                               command=lambda i=item, t=item_type: self.add_to_cart(i, t))
                    add_button.pack(side="right")

        cart_button = ctk.CTkButton(self.current_frame, text="View Cart", command=self.show_cart)
        cart_button.pack(pady=(20, 10))

        logout_button = ctk.CTkButton(self.current_frame, text="Logout", command=self.show_login_frame)
        logout_button.pack(pady=(10, 10))

    def show_cart(self):
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self, corner_radius=15)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

        cart_label = ctk.CTkLabel(self.current_frame, text="Your Cart", font=ctk.CTkFont(size=24, weight="bold"))
        cart_label.pack(pady=(10, 20))

        total_price = 0
        if self.cart:
            for idx, item in enumerate(self.cart):
                item_frame = ctk.CTkFrame(self.current_frame)
                item_frame.pack(pady=(2, 2), fill="x")

                item_label = ctk.CTkLabel(item_frame, text=f"{item['type']}: {item['name']} - ${item['price']}")
                item_label.pack(side="left")

                remove_button = ctk.CTkButton(item_frame, text="Remove",
                                              command=lambda i=idx: self.remove_from_cart(i))
                remove_button.pack(side="right")

                total_price += item['price']

            total_label = ctk.CTkLabel(self.current_frame, text=f"Total: ${total_price:.2f}",
                                       font=ctk.CTkFont(size=16, weight="bold"))
            total_label.pack(pady=(10, 10))
        else:
            empty_label = ctk.CTkLabel(self.current_frame, text="Your cart is empty.")
            empty_label.pack(pady=(10, 10))

        place_order_button = ctk.CTkButton(self.current_frame, text="Place Order", command=self.place_order)
        place_order_button.pack(pady=(10, 5))

        cancel_order_button = ctk.CTkButton(self.current_frame, text="Cancel Order", command=self.cancel_order)
        cancel_order_button.pack(pady=(5, 5))

        back_button = ctk.CTkButton(self.current_frame, text="Back to Menu", command=self.show_menu_frame)
        back_button.pack(pady=(10, 10))

    def place_order(self):
        if not self.cart:
            self.display_message("Your cart is empty.", "red")
            return

        try:
            order_items = ", ".join([f"{item['type']} {item['name']}" for item in self.cart])
            total_price = sum(item['price'] for item in self.cart)
            new_order = Order(
                order_date=datetime.now(),
                customer_name=self.session.query(Customer).filter_by(Id=self.current_user_id).first().name,
                customer_gender=self.session.query(Customer).filter_by(Id=self.current_user_id).first().gender,
                customer_birthdate=self.session.query(Customer).filter_by(Id=self.current_user_id).first().birthdate,
                customer_phone="",  # Assuming you have a phone number field or adjust accordingly
                customer_address=self.session.query(Customer).filter_by(Id=self.current_user_id).first().address,
                is_discount_applied=False,  # Adjust as needed
                total_price=total_price,
                customer_id=self.current_user_id,
                status="Pending"
            )
            self.item_handler.session.add(new_order)
            self.item_handler.session.commit()
            self.display_message("Order placed successfully!", "green")
            self.cart = []  # Clear the cart
        except Exception as e:
            self.item_handler.session.rollback()
            self.display_message("Failed to place order.", "red")
            print(f"Error placing order: {e}")

    def cancel_order(self):
        self.cart = []
        self.show_menu_frame()

    def add_to_cart(self, item, item_type):
        self.cart.append({
            'id': item.Id,  # Use 'Id' with capital 'I'
            'name': item.name,
            'price': item.price,
            'type': item_type
        })
        self.display_message(f"Added {item.name} to cart.", "green")

    def remove_from_cart(self, index):
        removed_item = self.cart.pop(index)
        self.display_message(f"Removed {removed_item['name']} from cart.", "red")
        self.show_cart()

    def display_message(self, message, color):
        message_label = ctk.CTkLabel(self.current_frame, text=message, text_color="white",
                                     fg_color=color, corner_radius=10)
        message_label.pack(pady=(5, 10))
        self.after(1500, message_label.destroy)

    def show_admin_menu_frame(self):
        self.clear_frame()
        self.current_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.current_frame.pack(pady=50, padx=50, fill="both", expand=True)

        admin_menu_label = ctk.CTkLabel(self.current_frame, text="Admin Menu",
                                        font=ctk.CTkFont(size=24, weight="bold"))
        admin_menu_label.pack(pady=(10, 20))

        add_item_button = ctk.CTkButton(self.current_frame, text="Add Item", command=self.show_add_item_frame)
        add_item_button.pack(pady=(10, 10))

        update_item_button = ctk.CTkButton(self.current_frame, text="Update Item",
                                           command=self.show_update_item_frame)
        update_item_button.pack(pady=(10, 10))

        delete_item_button = ctk.CTkButton(self.current_frame, text="Delete Item",
                                           command=self.show_delete_item_frame)
        delete_item_button.pack(pady=(10, 10))

        view_pizzas_button = ctk.CTkButton(self.current_frame, text="View Pizzas", command=self.show_view_pizzas)
        view_pizzas_button.pack(pady=(10, 10))

        logout_button = ctk.CTkButton(self.current_frame, text="Logout", command=self.show_login_frame)
        logout_button.pack(pady=(20, 10))

    def show_view_pizzas(self):
        self.clear_frame()
        self.current_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

        pizzas = self.item_handler.get_items("Pizza")

        view_label = ctk.CTkLabel(self.current_frame, text="All Pizzas", font=ctk.CTkFont(size=24, weight="bold"))
        view_label.pack(pady=(10, 20))

        if pizzas:
            for pizza in pizzas:
                pizza_label = ctk.CTkLabel(
                    self.current_frame,
                    text=f"ID: {pizza.Id}, Name: {pizza.name}, Price: ${pizza.price}, "
                         f"Vegetarian: {pizza.is_vegetarian}, Vegan: {pizza.is_vegan}"
                )
                pizza_label.pack(pady=(5, 5))
        else:
            no_pizza_label = ctk.CTkLabel(self.current_frame, text="No pizzas available.")
            no_pizza_label.pack(pady=(10, 10))

        back_button = ctk.CTkButton(self.current_frame, text="Back", command=self.show_admin_menu_frame)
        back_button.pack(pady=(20, 10))

    def show_add_item_frame(self):
        self.clear_frame()
        self.current_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

        item_types = ["Pizza", "Drink", "Dessert"]
        self.selected_item_type = ctk.StringVar(value="Pizza")
        item_type_label = ctk.CTkLabel(self.current_frame, text="Select Item Type:")
        item_type_label.pack(pady=(10, 5))
        item_type_dropdown = ctk.CTkOptionMenu(self.current_frame, values=item_types,
                                               variable=self.selected_item_type,
                                               command=self.update_add_item_fields)
        item_type_dropdown.pack(pady=(5, 20))

        self.add_item_fields_frame = ctk.CTkFrame(self.current_frame)
        self.add_item_fields_frame.pack(pady=(5, 20), fill="both", expand=True)

        self.update_add_item_fields(self.selected_item_type.get())
        save_button = ctk.CTkButton(self.current_frame, text="Save",
                                    command=lambda: self.save_item(self.selected_item_type.get()))
        save_button.pack(pady=(10, 10))
        back_button = ctk.CTkButton(self.current_frame, text="Back", command=self.show_admin_menu_frame)
        back_button.pack(pady=(10, 10))

    def show_update_item_frame(self):
        self.clear_frame()
        self.current_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

        item_types = ["Pizza", "Drink", "Dessert"]
        self.selected_item_type = ctk.StringVar(value="Pizza")
        item_type_label = ctk.CTkLabel(self.current_frame, text="Select Item Type:")
        item_type_label.pack(pady=(10, 5))
        item_type_dropdown = ctk.CTkOptionMenu(self.current_frame, values=item_types,
                                               variable=self.selected_item_type,
                                               command=self.update_update_item_fields)
        item_type_dropdown.pack(pady=(5, 20))

        self.update_item_fields_frame = ctk.CTkFrame(self.current_frame)
        self.update_item_fields_frame.pack(pady=(5, 20), fill="both", expand=True)

        self.update_update_item_fields(self.selected_item_type.get())
        update_button = ctk.CTkButton(self.current_frame, text="Update",
                                      command=lambda: self.update_item(self.selected_item_type.get()))
        update_button.pack(pady=(10, 10))
        back_button = ctk.CTkButton(self.current_frame, text="Back", command=self.show_admin_menu_frame)
        back_button.pack(pady=(10, 10))

    def show_delete_item_frame(self):
        self.clear_frame()
        self.current_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

        item_types = ["Pizza", "Drink", "Dessert"]
        self.selected_item_type = ctk.StringVar(value="Pizza")
        item_type_label = ctk.CTkLabel(self.current_frame, text="Select Item Type:")
        item_type_label.pack(pady=(10, 5))
        item_type_dropdown = ctk.CTkOptionMenu(self.current_frame, values=item_types,
                                               variable=self.selected_item_type)
        item_type_dropdown.pack(pady=(5, 20))

        self.item_id_entry = ctk.CTkEntry(self.current_frame, placeholder_text="Item ID to delete")
        self.item_id_entry.pack(pady=(10, 5))

        delete_button = ctk.CTkButton(self.current_frame, text="Delete",
                                      command=lambda: self.delete_item(self.selected_item_type.get()))
        delete_button.pack(pady=(10, 10))

        back_button = ctk.CTkButton(self.current_frame, text="Back", command=self.show_admin_menu_frame)
        back_button.pack(pady=(10, 10))

    def update_add_item_fields(self, item_type):
        for widget in self.add_item_fields_frame.winfo_children():
            widget.destroy()

        self.name_entry = ctk.CTkEntry(self.add_item_fields_frame, placeholder_text=f"{item_type} Name")
        self.name_entry.pack(pady=(10, 5))
        self.price_entry = ctk.CTkEntry(self.add_item_fields_frame, placeholder_text="Price")
        self.price_entry.pack(pady=(10, 5))

        if item_type == "Pizza":
            self.is_vegetarian_var = ctk.BooleanVar()
            self.is_vegan_var = ctk.BooleanVar()
            vegetarian_checkbox = ctk.CTkCheckBox(self.add_item_fields_frame, text="Vegetarian",
                                                  variable=self.is_vegetarian_var)
            vegetarian_checkbox.pack(pady=(10, 5))
            vegan_checkbox = ctk.CTkCheckBox(self.add_item_fields_frame, text="Vegan", variable=self.is_vegan_var)
            vegan_checkbox.pack(pady=(10, 5))

    def update_update_item_fields(self, item_type):
        for widget in self.update_item_fields_frame.winfo_children():
            widget.destroy()

        self.item_id_entry = ctk.CTkEntry(self.update_item_fields_frame, placeholder_text="Item ID")
        self.item_id_entry.pack(pady=(10, 5))

        self.name_entry = ctk.CTkEntry(self.update_item_fields_frame, placeholder_text=f"{item_type} Name")
        self.name_entry.pack(pady=(10, 5))
        self.price_entry = ctk.CTkEntry(self.update_item_fields_frame, placeholder_text="Price")
        self.price_entry.pack(pady=(10, 5))

        if item_type == "Pizza":
            self.is_vegetarian_var = ctk.BooleanVar()
            self.is_vegan_var = ctk.BooleanVar()
            vegetarian_checkbox = ctk.CTkCheckBox(self.update_item_fields_frame, text="Vegetarian",
                                                  variable=self.is_vegetarian_var)
            vegetarian_checkbox.pack(pady=(10, 5))
            vegan_checkbox = ctk.CTkCheckBox(self.update_item_fields_frame, text="Vegan",
                                             variable=self.is_vegan_var)
            vegan_checkbox.pack(pady=(10, 5))

    def save_item(self, item_type):
        name = self.name_entry.get()
        price_text = self.price_entry.get()
        if not name or not price_text:
            self.display_message("Name and Price are required.", "red")
            return

        try:
            price = float(price_text)
        except ValueError:
            self.display_message("Invalid price format.", "red")
            return

        if item_type == "Pizza":
            is_vegetarian = self.is_vegetarian_var.get()
            is_vegan = self.is_vegan_var.get()
            success = self.item_handler.add_item(item_type, name, price,
                                                 is_vegetarian=is_vegetarian, is_vegan=is_vegan)
        else:
            success = self.item_handler.add_item(item_type, name, price)

        if success:
            self.display_message(f"{item_type} '{name}' added successfully.", "green")
            self.show_admin_menu_frame()
        else:
            self.display_message(f"Failed to add {item_type}.", "red")

    def update_item(self, item_type):
        item_id_text = self.item_id_entry.get()
        name = self.name_entry.get()
        price_text = self.price_entry.get()

        if not item_id_text:
            self.display_message("Item ID is required.", "red")
            return

        try:
            item_id = int(item_id_text)
        except ValueError:
            self.display_message("Invalid Item ID format.", "red")
            return

        price = None
        if price_text:
            try:
                price = float(price_text)
            except ValueError:
                self.display_message("Invalid price format.", "red")
                return

        kwargs = {}
        if item_type == "Pizza":
            kwargs['is_vegetarian'] = self.is_vegetarian_var.get()
            kwargs['is_vegan'] = self.is_vegan_var.get()

        success = self.item_handler.update_item(item_type, item_id, name, price, **kwargs)

        if success:
            self.display_message(f"{item_type} ID {item_id} updated successfully.", "green")
            self.show_admin_menu_frame()
        else:
            self.display_message(f"Failed to update {item_type}.", "red")

    def delete_item(self, item_type):
        item_id_text = self.item_id_entry.get()

        if not item_id_text:
            self.display_message("Item ID is required.", "red")
            return

        try:
            item_id = int(item_id_text)
        except ValueError:
            self.display_message("Invalid Item ID format.", "red")
            return

        success = self.item_handler.delete_item(item_type, item_id)

        if success:
            self.display_message(f"{item_type} ID {item_id} deleted successfully.", "green")
            self.show_admin_menu_frame()
        else:
            self.display_message(f"Failed to delete {item_type}.", "red")

    def login_customer(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        login_result = self.customer_handler.login_customer(username, password)
        if login_result:
            self.current_user_id = login_result[1]
            self.show_menu_frame()
        else:
            self.display_message("Login failed! Invalid credentials.", "red")

    def login_admin(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.customer_handler.login_admin(username, password):
            self.show_admin_menu_frame()
        else:
            self.display_message("Admin login failed! Invalid credentials.", "red")

    def register_customer(self):
        name = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.reg_confirm_password_entry.get()
        gender = self.reg_gender_entry.get()
        birthdate = self.reg_birthdate_entry.get()
        address = self.reg_address_entry.get()

        if not name or not password or not confirm_password:
            self.display_message("Username and Password fields are required.", "red")
            return

        if password != confirm_password:
            self.display_message("Passwords do not match.", "red")
            return

        success = self.customer_handler.register_customer(name, gender, birthdate, address, password)
        if success:
            self.display_message("Registered successfully! Please log in.", "green")
            self.show_login_frame()
        else:
            self.display_message(f"Registration failed for user '{name}'.", "red")


if __name__ == "__main__":
    app = ItemGUI()
    app.mainloop()
