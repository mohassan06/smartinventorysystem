# product.py
# Product class for Smart Inventory Management System
# Author: Paramveer

class Product:
    # Static category list
    CATEGORIES = [
        "Electronics", "Clothing", "Home", "Grocery", "Books",
        "Toys", "Sports", "Beauty", "Automotive", "Others"
    ]

    def __init__(self, product_id, name, category, quantity=0, price=0.0, reorder_level=0):
        self.__product_id = product_id
        self.__name = name
        self.__category = category   
        self.__quantity = quantity
        self.__price = price
        self.__reorder_level = reorder_level

    # ===== Getters =====
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_category(self):
        return self.__category

    def get_quantity(self):
        return self.__quantity

    def get_price(self):
        return self.__price

    def get_reorder_level(self):
        return self.__reorder_level

    def get_category_name(self):
        # Maps integer to category name
        if 1 <= self.__category <= len(Product.CATEGORIES):
            return Product.CATEGORIES[self.__category - 1]
        return "Unknown"

    # ===== Setters (except quantity) =====
    def set_product_id(self, product_id):
        self.__product_id = product_id

    def set_name(self, name):
        self.__name = name

    def set_category(self, category):
        self.__category = category

    def set_price(self, price):
        self.__price = price

    def set_reorder_level(self, reorder_level):
        self.__reorder_level = reorder_level

    # ===== Business Logic =====
    def needs_restock(self):
        return self.__quantity <= self.__reorder_level

    def restock(self, amount):
        if amount > 0:
            self.__quantity += amount

    def sell(self, amount):
        if 0 < amount <= self.__quantity:
            self.__quantity -= amount
            return True
        return False

    # ===== String Representation =====
    def __str__(self):
        return f"{self.__product_id} {self.__name} {self.get_category_name()} {self.__quantity} {self.__price:.2f} $"



