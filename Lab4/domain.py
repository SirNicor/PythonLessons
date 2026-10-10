import json


class ProductNotFoundError(Exception):
    """Исключение при отсутствии товара"""
    pass


class Product:
    def __init__(self, article, name, category, price, quantity):
        self.article = article
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity

    def change_price(self, new_price):
        if new_price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.price = new_price

    def change_quantity(self, new_quantity):
        if new_quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        self.quantity = new_quantity

    def to_dict(self):
        return {
            "article": self.article,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            article=data["article"],
            name=data["name"],
            category=data["category"],
            price=data["price"],
            quantity=data["quantity"],
        )

    def __str__(self):
        return (f"[{self.article}] {self.name} | Категория: {self.category} | "
                f"Цена: {self.price:.2f} | Кол-во: {self.quantity}")

    def __eq__(self, other):
        return self.article == other.article

    def __lt__(self, other):
        return self.price < other.price