import json
import os
from domain import Product


DEFAULT_FILE = "products.json"


def save_products(products, filepath=DEFAULT_FILE):
    """Сохранение списка товаров в JSON"""
    data = [p.to_dict() for p in products]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Сохранено {len(data)} товаров в {filepath}")


def load_products(filepath=DEFAULT_FILE):
    """Загрузка списка товаров из JSON"""
    if not os.path.exists(filepath):
        print(f"Файл {filepath} не найден. Создан пустой список.")
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    products = [Product.from_dict(item) for item in data]
    print(f"Загружено {len(products)} товаров из {filepath}")
    return products
