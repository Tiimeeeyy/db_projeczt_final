Project Description
In response to recent EU regulations that have banned centralized take-away ordering services for pizza restaurants, each restaurant in Europe is now required to operate its own independent pizza ordering system. This project aims to develop a comprehensive software solution for a pizza restaurant, enabling it to manage its own ordering, processing, and delivery operations effectively.

Given the expertise of pizza restaurants in software architecture design, they have decided to adopt a well-structured, modular approach by separating the concerns of models, controllers, and views within the system. This separation aligns with best practices in software engineering, ensuring that the system is scalable, maintainable, and easy to extend in the future.

While some of you may have already worked on a controller for a similar system during your Software Engineering course, this project will focus on building and integrating the model layer, as well as expanding the system’s overall functionality to meet the specific needs of a modern pizza restaurant.

Software Requirements
Menu Presentation
The first critical feature of the system is the ability to present a comprehensive and dynamic menu to customers. This menu will include:

Pizza Listings: A list of all available pizzas at the restaurant, each with detailed information.
Ingredients: Display all ingredients used in each pizza.
Price Calculation: Show the price of each pizza, calculated based on the sum of its ingredient costs, a 40% profit margin, and the inclusion of a 9% VAT.
Dietary Information: Indicate whether each pizza is vegetarian or vegan based on its ingredients.
Additional Items: The menu should also list drinks and desserts.
The menu must include at least 10 distinct pizzas, featuring at least 10 different ingredients, along with 4 drinks and 2 desserts.
This menu is the first point of interaction between the customer and the system, so it must be user-friendly and informative. Additionally, it should demonstrate the software’s ability to dynamically calculate and present pricing based on the ingredients and other factors.

Order Processing
The system must also manage the complete process of taking and processing orders, including:

Order Placement: Allow customers to place orders for pizzas, drinks, and desserts. Each order must include at least one pizza.
Customer Information Management: Store essential customer information such as name, gender, birthdate, phone number, and address. This information is crucial for order confirmation and delivery.
Customer Accounts and Discounts:
Implement a simple login system for customers, which does not need to be highly secure.
Track the number of pizzas each customer has ordered. After 10 pizzas, customers should automatically receive a 10% discount on their next order.
Customers can also receive and redeem a discount code, which must be validated during the order process. The code can only be used once.
Offer customers a free pizza and drink on their birthday, requiring the system to check the date and apply the appropriate offer.
Order Confirmation: Upon placing an order, customers should receive a confirmation with details of their order and an estimated delivery time.
Restaurant Monitoring: Provide a real-time display for the restaurant staff, showing a list of pizzas that have been ordered but not yet dispatched for delivery.
Earnings Report: Generate a monthly earnings report for the restaurant, with filtering options based on region (postal code or city), customer gender, and age.
Order Delivery
Delivery management is another crucial component, involving:

Delivery Status: Allow customers to check the current status of their order (e.g., being prepared, in process, out for delivery) and estimated delivery time.
Order Cancellation: Customers should be able to cancel their order within 5 minutes of placing it.
Delivery Personnel Management:
The restaurant employs several delivery persons, each assigned to a specific postal code area.
A delivery person can only deliver within their assigned area. Multiple delivery persons can be assigned to the same postal code if needed.
Once a delivery is initiated, the delivery person is unavailable for further deliveries for 30 minutes.
The system must handle the delivery timing logic, including the ability to group multiple orders for the same postal code into a single delivery if they occur within a 3-minute window. With a maximum batch of 3 pizzas.
The basic delivery system described above meets the minimum requirements. However, the system is open to enhancements for those who wish to implement more efficient or advanced delivery logic, such as optimizing routes or managing delivery queues more effectively.