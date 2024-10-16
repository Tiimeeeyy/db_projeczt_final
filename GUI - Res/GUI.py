import customtkinter as ctk
from sqlalchemy import create_engine, exc, func, extract
from sqlalchemy.orm import sessionmaker
from models import Base, Customer, Pizza, Drink, Dessert, Admin, Order, DeliveryPersonnel
from datetime import datetime
import bcrypt
from order import OrderStatusTracker


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


class CustomerHandling:
    def __init__(self, db_url):
        try:
            engine = create_engine(db_url)
            Base.metadata.create_all(engine)
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
            return "customer", customer.Id
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
            Base.metadata.create_all(engine)
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

        self.staff_op_handler = StaffOp("mysql+pymysql://root:Porto123@localhost/pizza_db")
        self.customer_handler = CustomerHandling("mysql+pymysql://root:Porto123@localhost/pizza_db")
        self.item_handler = ItemHandling("mysql+pymysql://root:Porto123@localhost/pizza_db")
        self.order_tracker = OrderStatusTracker("mysql+pymysql://root:Porto123@localhost/pizza_db")
        self.title("1453-Items")
        self.geometry("500x600")
        self.resizable(False, False)

        self.current_frame = None
        self.current_user_id = None
        self.cart = []

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
            total_price = sum(item['price'] for item in self.cart)
            customer = self.customer_handler.session.query(Customer).filter_by(Id=self.current_user_id).first()
            if not customer:
                self.display_message("Customer not found.", "red")
                return

            new_order = Order(
                order_date=datetime.now(),
                customer_name=customer.name,
                customer_gender=customer.gender,
                customer_birthdate=customer.birthdate,
                customer_phone="",
                customer_address=customer.address,
                is_discount_applied=False,
                total_price=total_price,
                customer_id=self.current_user_id,
                status="Pending"
            )


            self.item_handler.session.add(new_order)
            self.item_handler.session.flush()


            for cart_item in self.cart:
                item_type = cart_item['type']
                item_id = cart_item['id']
                if item_type == "Pizza":
                    pizza = self.item_handler.session.query(Pizza).filter_by(Id=item_id).first()
                    if pizza:
                        new_order.pizzas.append(pizza)
                elif item_type == "Drink":
                    drink = self.item_handler.session.query(Drink).filter_by(Id=item_id).first()
                    if drink:
                        new_order.drinks.append(drink)
                elif item_type == "Dessert":
                    dessert = self.item_handler.session.query(Dessert).filter_by(Id=item_id).first()
                    if dessert:
                        new_order.desserts.append(dessert)

            self.item_handler.session.commit()

            self.display_message("Order placed successfully!", "green")
            self.order_tracker.start_tracking(new_order.Id)
            self.cart = []
        except Exception as e:
            self.item_handler.session.rollback()
            self.display_message("Failed to place order.", "red")
            print(f"Error placing order: {e}")

    def cancel_order(self):
        self.cart = []
        self.show_menu_frame()

    def add_to_cart(self, item, item_type):
        item_id = item.Id

        for cart_item in self.cart:
            if cart_item['id'] == item_id and cart_item['type'] == item_type:
                cart_item['quantity'] += 1
                self.display_message(f"Increased quantity of {item.name} in cart.", "green")
                return

        self.cart.append({
            'id': item_id,
            'name': item.name,
            'price': item.price,
            'type': item_type,
            'quantity': 1
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
        view_personnel_button = ctk.CTkButton(self.current_frame, text="View Personnel",
                                              command=self.show_view_personnel)
        view_personnel_button.pack(pady=(10, 10))

        generate_report_button = ctk.CTkButton(self.current_frame, text="Generate Monthly Report",
                                               command=self.show_generate_report_frame)
        generate_report_button.pack(pady=(10, 10))

        logout_button = ctk.CTkButton(self.current_frame, text="Logout", command=self.show_login_frame)
        logout_button.pack(pady=(20, 10))

    def show_view_personnel(self):
        self.clear_frame()
        self.current_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

        personnel = self.staff_op_handler.get_delivery_personnel()

        view_label = ctk.CTkLabel(self.current_frame, text="Delivery Personnel", font=ctk.CTkFont(size=24, weight="bold"))
        view_label.pack(pady=(10, 20))

        if personnel:
            for person in personnel:
                person_id = person.Id if hasattr(person, 'Id') else person.id
                person_label = ctk.CTkLabel(
                    self.current_frame,
                    text=f"ID: {person_id}, Name: {person.name}, Postal Code: {person.postal_code}, "
                         f"Available: {'Yes' if person.available else 'No'}"
                )
                person_label.pack(pady=(5, 5))

                if person.available:
                    assign_button = ctk.CTkButton(self.current_frame, text="Assign to Order",
                                                  command=lambda p=person: self.assign_rider(p))
                    assign_button.pack(pady=(0, 10))
        else:
            no_person_label = ctk.CTkLabel(self.current_frame, text="No personnel available.")
            no_person_label.pack(pady=(10, 10))

        back_button = ctk.CTkButton(self.current_frame, text="Back", command=self.show_admin_menu_frame)
        back_button.pack(pady=(20, 10))

    def assign_rider(self, person):

        pending_order = self.staff_op_handler.session.query(Order).filter_by(status="Pending").first()
        if pending_order:
            result = self.staff_op_handler.assign_rider_to_order(pending_order)
            self.display_message(result, "green" if "assigned" in result else "red")
            self.show_view_personnel()
        else:
            self.display_message("No pending orders found.", "red")

    def show_generate_report_frame(self):
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self, corner_radius=15)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

        report_label = ctk.CTkLabel(self.current_frame, text="Generate Monthly Earnings Report",
                                     font=ctk.CTkFont(size=24, weight="bold"))
        report_label.pack(pady=(10, 20))

        postal_code_label = ctk.CTkLabel(self.current_frame, text="Enter Postal Code Prefix (3 digits):")
        postal_code_label.pack(pady=(10, 5))

        self.postal_code_entry = ctk.CTkEntry(self.current_frame, placeholder_text="e.g., 123")
        self.postal_code_entry.pack(pady=(5, 10))

        generate_button = ctk.CTkButton(self.current_frame, text="Generate Report", command=self.generate_report)
        generate_button.pack(pady=(10, 10))

        back_button = ctk.CTkButton(self.current_frame, text="Back", command=self.show_admin_menu_frame)
        back_button.pack(pady=(10, 10))

    def generate_report(self):
        postal_code_prefix = self.postal_code_entry.get()
        if not postal_code_prefix or len(postal_code_prefix) != 3:
            self.display_message("Invalid postal code prefix. Please enter 3 digits.", "red")
            return

        monthly_earnings = self.staff_op_handler.generate_monthly_earnings_report(postal_code_prefix)


        report_result_label = ctk.CTkLabel(self.current_frame,
                                           text=f"Monthly earnings for postal code prefix '{postal_code_prefix}': ${monthly_earnings:.2f}",
                                           text_color="white", fg_color="green", corner_radius=10)
        report_result_label.pack(pady=(5, 10))


    def show_view_pizzas(self):
        self.clear_frame()
        self.current_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.current_frame.pack(pady=20, padx=20, fill="both", expand=True)

        pizzas = self.item_handler.get_items("Pizza")

        view_label = ctk.CTkLabel(self.current_frame, text="All Pizzas", font=ctk.CTkFont(size=24, weight="bold"))
        view_label.pack(pady=(10, 20))

        if pizzas:
            for pizza in pizzas:
                pizza_id = pizza.Id
                pizza_label = ctk.CTkLabel(
                    self.current_frame,
                    text=f"ID: {pizza_id}, Name: {pizza.name}, Price: ${pizza.price}, "
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
                query = query.filter(Order.customer_address.like(f"{postal_code_prefix}%"))

            monthly_earnings = query.scalar()
            return monthly_earnings if monthly_earnings else 0.0

        except Exception as e:
            print(f"An error occurred while generating monthly earnings report: {e}")
            return 0.0

    def get_delivery_personnel(self):
        try:
            personnel = self.session.query(DeliveryPersonnel).all()
            return personnel
        except Exception as e:
            print(f"An error occurred while fetching delivery personnel: {e}")
            return []

    def assign_rider_to_order(self, order):
        try:
            rider = self.session.query(DeliveryPersonnel).filter_by(available=True).first()

            if rider:
                order.delivery_person = rider
                order.assigned_time = datetime.now()
                rider.available = False
                self.session.commit()
                return f"Rider {rider.name} assigned to order {order.id}."
            else:
                return "No riders available at the moment."

        except Exception as e:
            return f"Error assigning rider: {e}"

if __name__ == "__main__":
    app = ItemGUI()
    app.mainloop()
