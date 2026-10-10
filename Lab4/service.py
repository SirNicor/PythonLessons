import random
from domain import Product, ProductNotFoundError


def check_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                raise ValueError
            if max_val is not None and value > max_val:
                raise ValueError
        except ValueError:
            range_msg = ""
            if min_val is not None and max_val is not None:
                range_msg = f" (от {min_val} до {max_val})"
            elif min_val is not None:
                range_msg = f" (не меньше {min_val})"
            print(f"Неверный ввод{range_msg}. Попробуйте снова.")
        else:
            return value


def check_float(prompt, min_val=None):
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                raise ValueError
        except ValueError:
            msg = f" (не меньше {min_val})" if min_val is not None else ""
            print(f"Неверный ввод{msg}. Попробуйте снова.")
        else:
            return value


def check_choice(prompt, options):
    while True:
        try:
            value = int(input(prompt))
            if value not in options:
                raise ValueError
        except ValueError:
            print(f"Введите одно из: {options}")
        else:
            return value


def add_product(products):
    article = input("Введите артикул: ").strip()
    if any(p.article == article for p in products):
        print(f"Товар с артикулом {article} уже существует!")
        return
    name = input("Введите название: ").strip()
    category = input("Введите категорию: ").strip()
    price = check_float("Введите цену: ", min_val=0)
    quantity = check_int("Введите количество: ", min_val=0)
    product = Product(article, name, category, price, quantity)
    products.append(product)
    print(f"Товар '{name}' добавлен.")


def change_price(products):
    article = input("Введите артикул товара: ").strip()
    product = _find_by_article(products, article)
    new_price = check_float("Введите новую цену: ", min_val=0)
    product.change_price(new_price)
    print(f"Цена товара '{product.name}' изменена на {new_price:.2f}")


def change_quantity(products):
    article = input("Введите артикул товара: ").strip()
    product = _find_by_article(products, article)
    new_qty = check_int("Введите новое количество: ", min_val=0)
    product.change_quantity(new_qty)
    print(f"Количество товара '{product.name}' изменено на {new_qty}")


def search_by_article(products):
    article = input("Введите артикул для поиска: ").strip()
    product = _find_by_article(products, article)
    print(f"Найден: {product}")


def search_by_name(products):
    name = input("Введите название (часть): ").strip().lower()
    found = [p for p in products if name in p.name.lower()]
    if not found:
        raise ProductNotFoundError(f"Товары с '{name}' не найдены")
    print(f"Найдено {len(found)} товаров:")
    for p in found:
        print(f"  {p}")


def filter_by_category(products):
    category = input("Введите категорию: ").strip().lower()
    filtered = [p for p in products if category in p.category.lower()]
    if not filtered:
        raise ProductNotFoundError(f"Категория '{category}' не найдена")
    print(f"Найдено {len(filtered)} товаров:")
    for p in filtered:
        print(f"  {p}")


def filter_by_price_range(products):
    min_price = check_float("Минимальная цена: ", min_val=0)
    max_price = check_float("Максимальная цена: ", min_val=min_price)
    filtered = [p for p in products if min_price <= p.price <= max_price]
    if not filtered:
        raise ProductNotFoundError("Товары в заданном диапазоне не найдены")
    print(f"Найдено {len(filtered)} товаров:")
    for p in filtered:
        print(f"  {p}")


def sort_by_price(products):
    if not products:
        print("Список пуст.")
        return
    sorted_products = sorted(products)
    print("Товары отсортированы по цене:")
    for p in sorted_products:
        print(f"  {p}")


def sort_by_quantity(products):
    if not products:
        print("Список пуст.")
        return
    sorted_products = sorted(products, key=lambda p: p.quantity)
    print("Товары отсортированы по количеству:")
    for p in sorted_products:
        print(f"  {p}")


def show_all(products):
    if not products:
        print("Список товаров пуст.")
        return
    for i, p in enumerate(products, 1):
        print(f"{i}. {p}")


def delete_product(products):
    article = input("Введите артикул товара для удаления: ").strip()
    product = _find_by_article(products, article)
    products.remove(product)
    print(f"Товар '{product.name}' удалён.")


def generate_random_products(products, count=None):
    if count is None:
        count = check_int("Сколько случайных товаров создать? ", min_val=1, max_val=20)
    categories = ["Электроника", "Одежда", "Книги", "Продукты", "Игрушки"]
    names = ["Ноутбук", "Смартфон", "Футболка", "Джинсы", "Роман", "Учебник",
             "Молоко", "Хлеб", "Мишка", "Конструктор", "Монитор", "Наушники"]
    for i in range(count):
        article = f"ART{random.randint(1000, 9999)}"
        while any(p.article == article for p in products):
            article = f"ART{random.randint(1000, 9999)}"
        product = Product(
            article=article,
            name=random.choice(names),
            category=random.choice(categories),
            price=round(random.uniform(100, 50000), 2),
            quantity=random.randint(0, 100),
        )
        products.append(product)
    print(f"Создано {count} случайных товаров.")


def _find_by_article(products, article):
    for p in products:
        if p.article == article:
            return p
    raise ProductNotFoundError(f"Товар с артикулом '{article}' не найден")