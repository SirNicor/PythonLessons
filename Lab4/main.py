import random
from domain import ProductNotFoundError
from storage import save_products, load_products
from service import (
    add_product, change_price, change_quantity,
    search_by_article, search_by_name,
    filter_by_category, filter_by_price_range,
    sort_by_price, sort_by_quantity,
    show_all, delete_product, generate_random_products,
    check_choice,
)


def main():
    products = []
    filepath = "products.json"

    print("Загрузить товары из файла? (1 - да, 2 - нет)")
    if check_choice("Ваш выбор: ", [1, 2]) == 1:
        products = load_products(filepath)

    while True:
        print("\n===== МЕНЮ =====")
        print("1. Показать все товары")
        print("2. Добавить товар")
        print("3. Изменить цену")
        print("4. Изменить количество")
        print("5. Поиск по артикулу")
        print("6. Поиск по названию")
        print("7. Фильтрация по категории")
        print("8. Фильтрация по диапазону цен")
        print("9. Сортировка по цене")
        print("10. Сортировка по количеству")
        print("11. Удалить товар")
        print("12. Сгенерировать случайные товары")
        print("13. Сохранить в JSON")
        print("14. Загрузить из JSON")
        print("0. Выход")

        choice = check_choice("Ваш выбор: ", list(range(0, 15)))

        try:
            if choice == 1:
                show_all(products)
            elif choice == 2:
                add_product(products)
            elif choice == 3:
                change_price(products)
            elif choice == 4:
                change_quantity(products)
            elif choice == 5:
                search_by_article(products)
            elif choice == 6:
                search_by_name(products)
            elif choice == 7:
                filter_by_category(products)
            elif choice == 8:
                filter_by_price_range(products)
            elif choice == 9:
                sort_by_price(products)
            elif choice == 10:
                sort_by_quantity(products)
            elif choice == 11:
                delete_product(products)
            elif choice == 12:
                generate_random_products(products)
            elif choice == 13:
                save_products(products, filepath)
            elif choice == 14:
                products = load_products(filepath)
            elif choice == 0:
                print("Сохранить перед выходом? (1 - да, 2 - нет)")
                if check_choice("Ваш выбор: ", [1, 2]) == 1:
                    save_products(products, filepath)
                break
        except ProductNotFoundError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()