import random
from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, name, price):
        self.name = name
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        self._price = value

    @abstractmethod
    def calculate_delivery(self, distance):
        pass

    def __str__(self):
        return f"{self.name} (Цена: {self.price:.2f})"

    def __lt__(self, other):
        return self.price < other.price

class PhysicalProduct(Product):
    def __init__(self, name, price, weight):
        super().__init__(name, price)
        self.weight = weight

    def calculate_delivery(self, distance):
        return self.weight * distance * 0.5

    def __str__(self):
        return f"{super().__str__()} | Физический | Вес: {self.weight} кг"

class DigitalProduct(Product):
    def __init__(self, name, price, file_size_mb):
        super().__init__(name, price)
        self.file_size_mb = file_size_mb

    def calculate_delivery(self, distance):
        return 0.0

    def __str__(self):
        return f"{super().__str__()} | Цифровой | Размер: {self.file_size_mb} МБ"

class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def get_total_price(self):
        return sum(p.price for p in self.products)

    def get_total_delivery(self, distance):
        return sum(p.calculate_delivery(distance) for p in self.products)

    def __str__(self):
        return f"Заказ #{self.order_id} | Товаров: {len(self.products)} | Сумма: {self.get_total_price():.2f}"

    def __add__(self, other):
        new_order = Order(f"{self.order_id}+{other.order_id}")
        new_order.products = self.products + other.products
        return new_order

    def __iter__(self):
        return iter(self.products)

    def __len__(self):
        return len(self.products)

def create_order(orders, next_id):
    print("Проверка на случайных данных - 1, ввод собственных данных - 2")
    change = checkTryCatch()
    order = Order(next_id)
    if change == 1:
        number_products = random.randint(1, 5)
        print(f"Количество товаров в заказе: {number_products}")
        phys_names = ["Ноутбук", "Смартфон", "Монитор", "Клавиатура", "Мышь"]
        dig_names = ["Игра", "Подписка", "Электронная книга", "Курс", "Лицензия"]
        for i in range(number_products):
            if random.choice([True, False]):
                name = random.choice(phys_names) + f" ({i+1})"
                price = random.randint(500, 100000)
                weight = random.randint(1, 20)
                product = PhysicalProduct(name, price, weight)
            else:
                name = random.choice(dig_names) + f" ({i+1})"
                price = random.randint(100, 5000)
                size = random.randint(10, 5000)
                product = DigitalProduct(name, price, size)
            order.add_product(product)
    else:
        number_products = int(input("Введите количество товаров в заказе: "))
        for i in range(number_products):
            print("Тип товара: 1 - Физический, 2 - Цифровой")
            p_type = checkTryCatch()
            if p_type == 1:
                while True:
                    try:
                        raw = input(f"Товар {i+1} (название цена вес), пример: Ноутбук 50000 2.5: ").split()
                        if len(raw) < 3:
                            raise IndexError
                        name = raw[0]
                        price = float(raw[1])
                        weight = float(raw[2])
                        if price < 0 or weight < 0:
                            raise ValueError
                    except (ValueError, IndexError):
                        print("Неверный формат. Пример: Ноутбук 50000 2.5")
                    else:
                        break
                product = PhysicalProduct(name, price, weight)
            else:
                while True:
                    try:
                        raw = input(f"Товар {i+1} (название цена размер_мб), Пример - Игра 2000 50.5 : ").split()
                        if len(raw) < 3:
                            raise IndexError
                        name = raw[0]
                        price = float(raw[1])
                        size = float(raw[2])
                        if price < 0 or size < 0:
                            raise ValueError
                    except (ValueError, IndexError):
                        print("Неверный формат. Пример: Игра 2000 50.5")
                    else:
                        break
                product = DigitalProduct(name, price, size)
            order.add_product(product)
    orders.append(order)
    print(f"Заказ #{next_id} создан.")
    return next_id + 1

def show_orders(orders):
    if len(orders) == 0:
        print("Список заказов пуст.")
        return
    for i, order in enumerate(orders):
        print(f"{i+1}. {order}")

def search_by_id(orders):
    while True:
        try:
            search_id = int(input("Введите ID заказа для поиска: "))
        except ValueError:
            print("Введите целое число.")
        else:
            break
    found = [o for o in orders if o.order_id == search_id]
    if len(found) == 0:
        print(f"Заказ с ID {search_id} не найден.")
    else:
        for order in found:
            print(f"  {order}")
            print("  Состав заказа:")
            for product in order:
                print(f"    {product}")
            dist = 10
            print(f"  Стоимость доставки на {dist} км: {order.get_total_delivery(dist):.2f}")

def filter_by_price(orders):
    while True:
        try:
            price = float(input("Показать заказы с суммой больше: "))
        except ValueError:
            print("Введите число.")
        else:
            break
    filtered = [o for o in orders if o.get_total_price() > price]
    if len(filtered) == 0:
        print(f"Заказов с суммой больше {price} не найдено.")
    else:
        print(f"Найдено заказов: {len(filtered)}")
        for order in filtered:
            print(f"  {order}")

def sort_by_items(orders):
    if len(orders) == 0:
        print("Список заказов пуст.")
        return
    sorted_orders = sorted(orders, key=lambda o: len(o))
    print("Заказы отсортированы по количеству товаров:")
    for order in sorted_orders:
        print(f"  {order}")

def show_statistics(orders):
    if len(orders) == 0:
        print("Список заказов пуст.")
        return
    total_items = sum(len(o) for o in orders)
    total_sum = sum(o.get_total_price() for o in orders)
    avg_sum = total_sum / len(orders)
    max_order = max(orders, key=lambda o: o.get_total_price())
    print(f"Всего заказов: {len(orders)}")
    print(f"Всего товаров: {total_items}")
    print(f"Общая сумма: {total_sum:.2f}")
    print(f"Средняя сумма заказа: {avg_sum:.2f}")
    print(f"Самый дорогой заказ: #{max_order.order_id} ({max_order.get_total_price():.2f})")

def merge_orders(orders):
    if len(orders) < 2:
        print("Недостаточно заказов для объединения.")
        return
    show_orders(orders)
    while True:
        try:
            id1 = int(input("Введите ID первого заказа: "))
            id2 = int(input("Введите ID второго заказа: "))
            if id1 == id2:
                raise ValueError
        except ValueError:
            print("Введите разные целые числа.")
        else:
            break
    o1 = next((o for o in orders if o.order_id == id1), None)
    o2 = next((o for o in orders if o.order_id == id2), None)
    if not o1 or not o2:
        print("Один или оба заказа не найдены.")
        return
    new_order = o1 + o2
    orders.append(new_order)
    print(f"Создан новый заказ #{new_order.order_id}")

def delete_order(orders):
    if len(orders) == 0:
        print("Список заказов пуст.")
        return
    show_orders(orders)
    while True:
        try:
            index = int(input("Введите номер заказа для удаления: "))
            if index < 1 or index > len(orders):
                raise IndexError
        except ValueError:
            print("Введите целое число.")
        except IndexError:
            print(f"Номер должен быть от 1 до {len(orders)}.")
        else:
            break
    removed = orders.pop(index - 1)
    print(f"Заказ #{removed.order_id} удален.")

def checkMenuChoice():
    while True:
        try:
            choice = int(input())
            if not (isinstance(choice, int)):
                raise TypeError
            if not (choice in range(0, 9)):
                raise IndexError
        except (TypeError, ValueError):
            print("Вы ввели не тот тип данных")
        except IndexError:
            print("Введите число от 0 до 8")
        else:
            break
    return choice

def checkTryCatch():
    while True:
        try:
            change = int(input())
            if not (isinstance(change, int)):
                raise TypeError
            if not (change in range(1, 3)):
                raise IndexError
        except (TypeError, ValueError):
            print("Вы ввели не тот тип данных")
        except IndexError:
            print("Не 1 и не 2")
        else:
            break
    return change

def main():
    while True:
        orders = []
        next_id = 1
        print("Проверка на случайных данных - 1, ввод собственных данных - 2")
        change = checkTryCatch()
        if change == 1:
            number_orders = random.randint(3, 8)
            print(f"Количество заказов: {number_orders}")
            for _ in range(number_orders):
                order = Order(next_id)
                num_prod = random.randint(1, 4)
                phys_names = ["Ноутбук", "Смартфон", "Монитор"]
                dig_names = ["Игра", "Подписка", "Книга"]
                for _ in range(num_prod):
                    if random.choice([True, False]):
                        order.add_product(PhysicalProduct(random.choice(phys_names), random.randint(1000, 50000), random.randint(1, 10)))
                    else:
                        order.add_product(DigitalProduct(random.choice(dig_names), random.randint(100, 5000), random.randint(10, 1000)))
                orders.append(order)
                next_id += 1
        else:
            number_orders = int(input("Введите количество заказов: "))
            for _ in range(number_orders):
                next_id = create_order(orders, next_id)

        while True:
            print("\n===== МЕНЮ =====")
            print("1. Создать заказ")
            print("2. Показать все заказы")
            print("3. Поиск заказа по ID")
            print("4. Фильтрация по сумме")
            print("5. Сортировка по количеству товаров")
            print("6. Статистика")
            print("7. Объединить два заказа")
            print("8. Удалить заказ")
            print("0. Выход")
            choice = checkMenuChoice()

            if choice == 1:
                next_id = create_order(orders, next_id)
            elif choice == 2:
                show_orders(orders)
            elif choice == 3:
                search_by_id(orders)
            elif choice == 4:
                filter_by_price(orders)
            elif choice == 5:
                sort_by_items(orders)
            elif choice == 6:
                show_statistics(orders)
            elif choice == 7:
                merge_orders(orders)
            elif choice == 8:
                delete_order(orders)
            elif choice == 0:
                break

        print("Если вы хотите повторить программу введите 1, иначе 2")
        change = checkTryCatch()
        if change == 2:
            break

if __name__ == "__main__":
    main()