classDiagram
direction BT
class customers {
   longtext Name
   longtext Gender
   datetime(6) Birthdate
   longtext Address
   longtext Password
   int Id
}
class desserts {
   longtext Name
   decimal(65,30) Price
   int DessertId
}
class drinks {
   longtext Name
   decimal(65,30) Price
   int Id
}
class ingredients {
   longtext Name
   decimal(65,30) Cost
   tinyint(1) IsVegitarian
   tinyint(1) IsVegan
   int Id
}
class orderdrinks {
   int OrderId
   int DrinkId
}
class orderpizzas {
   int OrderId
   int PizzaId
}
class orders {
   datetime(6) OrderDate
   longtext CustomerName
   longtext CustomerGender
   datetime(6) CustomerBirthdate
   longtext CustomerPhone
   longtext CustomerAddress
   tinyint(1) IsDiscountApplied
   decimal(65,30) TotalPrice
   int CustomerId
   int Id
}
class pizzaingredients {
   int PizzaId
   int IngredientId
}
class pizzas {
   longtext Name
   tinyint(1) IsVegetarian
   tinyint(1) IsVegan
   decimal(65,30) Price
   int Id
}

orderdrinks  -->  drinks : DrinkId:Id
orderdrinks  -->  orders : OrderId:Id
orderpizzas  -->  orders : OrderId:Id
orderpizzas  -->  pizzas : PizzaId:Id
orders  -->  customers : CustomerId:Id
pizzaingredients  -->  ingredients : IngredientId:Id
pizzaingredients  -->  pizzas : PizzaId:Id
