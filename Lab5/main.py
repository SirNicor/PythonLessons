import random
from models import Book, FictionBook, NonFictionBook, BookNotFoundError
from operations import (
    filter_objects, transform_objects, sort_objects,
    get_titles, get_authors, filter_by_rating, filter_by_year_range,
    sort_by_pages, sort_by_rating_desc, find_largest_book,
    get_total_pages, get_average_rating,
    has_author, all_books_above_rating,
    get_books_by_author_dict, get_unique_authors_set,
)
from generators import (
    books_by_period, books_by_author, high_rated_books,
    BookIterator, FilteredBookIterator, demonstrate_laziness,
)


def check_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                raise ValueError
            if max_val is not None and value > max_val:
                raise ValueError
        except ValueError:
            msg = ""
            if min_val is not None and max_val is not None:
                msg = f" (от {min_val} до {max_val})"
            elif min_val is not None:
                msg = f" (не меньше {min_val})"
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


def generate_random_books(count=10):
    authors = ["Толстой", "Достоевский", "Пушкин", "Чехов", "Гоголь", 
               "Булгаков", "Тургенев", "Лермонтов", "Гончаров", "Диккенс"]
    fiction_titles = ["Война и мир", "Преступление и наказание", "Евгений Онегин",
                      "Вишнёвый сад", "Мёртвые души", "Мастер и Маргарита",
                      "Анна Каренина", "Идиот", "Капитанская дочка", "Оливер Твист"]
    nonfiction_titles = ["Физика", "Математика", "Химия", "Биология", 
                         "История", "Философия", "Экономика", "Психология"]
    subjects = ["Физика", "Математика", "Химия", "Биология", "История"]
    
    books = []
    for i in range(count):
        author = random.choice(authors)
        year = random.randint(1800, 2024)
        pages = random.randint(50, 1200)
        rating = random.randint(40, 100)
        
        if random.choice([True, False]):
            title = random.choice(fiction_titles) + f" ({i+1})"
            books.append(FictionBook(title, author, year, pages, rating))
        else:
            title = random.choice(nonfiction_titles) + f" ({i+1})"
            subject = random.choice(subjects)
            books.append(NonFictionBook(title, author, year, pages, rating, subject))
    
    return books


def show_all(books):
    if not books:
        print("Список книг пуст.")
        return
    for i, book in enumerate(books, 1):
        print(f"{i}. {book}")


def demo_filter_by_rating(books):
    min_rating = check_int("Введите минимальный рейтинг (0-100): ", 0, 100)
    filtered = filter_by_rating(books, min_rating)
    print(f"\nКниги с рейтингом >= {min_rating}:")
    if filtered:
        for book in filtered:
            print(f"  {book}")
    else:
        print("  Таких книг не найдено.")


def demo_get_titles(books):
    titles = get_titles(books)
    print(f"\nНазвания всех книг (через map):")
    for title in titles:
        print(f"  - {title}")


def demo_sort_by_pages(books):
    sorted_books = sort_by_pages(books)
    print("\nКниги, отсортированные по количеству страниц:")
    for book in sorted_books:
        print(f"  {book}")


def demo_find_largest(books):
    largest = find_largest_book(books)
    if largest:
        print(f"\nСамая большая книга: {largest}")
        print(f"  Количество страниц: {largest.number_of_pages}")
    else:
        print("Список пуст.")


def demo_has_author(books):
    author = input("Введите имя автора для проверки: ").strip()
    exists = has_author(books, author)
    if exists:
        print(f"Книги автора '{author}' найдены.")
    else:
        print(f"Книги автора '{author}' не найдены.")


def demo_generator_period(books):
    start = check_int("Начальный год: ", 1000, 2100)
    end = check_int("Конечный год: ", start, 2100)
    print(f"\nКниги {start}-{end} годов (через генератор):")
    count = 0
    for book in books_by_period(books, start, end):
        print(f"  {book}")
        count += 1
    if count == 0:
        print("  Книг не найдено.")


def demo_iterator(books):
    print("\n=== Работа с собственным итератором ===")
    iterator = BookIterator(books)
    print("Первые 3 книги через next():")
    try:
        for _ in range(3):
            print(f"  {next(iterator)}")
    except StopIteration:
        print("  Книги закончились.")
    
    print("\nВсе книги через for (итератор автоматически):")
    for book in BookIterator(books[:5]):
        print(f"  {book}")


def demo_filtered_iterator(books):
    min_rating = check_int("Минимальный рейтинг для итератора: ", 0, 100)
    print(f"\nКниги с рейтингом >= {min_rating} (через FilteredBookIterator):")
    for book in FilteredBookIterator(books, min_rating):
        print(f"  {book}")


def demo_higher_order(books):
    print("\n=== Функции высшего порядка ===")
    
    expensive = filter_objects(books, lambda b: b.rating >= 80)
    print(f"Книги с рейтингом >= 80: {len(expensive)} шт.")
    
    categories = transform_objects(books, lambda b: b.get_category())
    print(f"Категории всех книг: {set(categories)}")
    
    by_rating = sort_objects(books, lambda b: b.rating, reverse=True)
    print(f"Топ-3 по рейтингу:")
    for b in by_rating[:3]:
        print(f"  {b}")


def demo_comprehensions(books):
    print("\n=== Comprehensions ===")
    
    authors = get_authors(books)
    print(f"Все авторы: {authors}")
    
    unique_authors = get_unique_authors_set(books)
    print(f"Уникальные авторы: {unique_authors}")
    
    by_author = get_books_by_author_dict(books)
    print(f"\nКниги по авторам:")
    for author, book_list in by_author.items():
        print(f"  {author}: {len(book_list)} кн.")


def demo_statistics(books):
    if not books:
        print("Список пуст.")
        return
    print("\n=== Статистика ===")
    print(f"Всего книг: {len(books)}")
    print(f"Общее количество страниц: {get_total_pages(books)}")
    print(f"Средний рейтинг: {get_average_rating(books):.2f}")
    
    all_high = all_books_above_rating(books, 50)
    print(f"Все книги имеют рейтинг >= 50: {all_high}")


def main():
    books = []
    
    print("=== Лабораторная работа №5: Книги ===\n")
    print("Сгенерировать случайные книги для демонстрации? (1 - да, 2 - нет)")
    if check_choice("Ваш выбор: ", [1, 2]) == 1:
        count = check_int("Сколько книг создать? ", 1, 30)
        books = generate_random_books(count)
        print(f"Создано {len(books)} книг.\n")

    while True:
        print("\n===== МЕНЮ =====")
        print("1. Показать все книги")
        print("2. Фильтрация по рейтингу (filter + lambda)")
        print("3. Получение названий (map + lambda)")
        print("4. Сортировка по страницам (sorted + key)")
        print("5. Поиск самой большой книги (reduce)")
        print("6. Проверка наличия автора (any)")
        print("7. Генератор книг заданного периода (yield)")
        print("8. Собственный итератор (__iter__, __next__)")
        print("9. Фильтрующий итератор")
        print("10. Функции высшего порядка")
        print("11. Comprehensions (list, set, dict)")
        print("12. Статистический анализ")
        print("13. Демонстрация ленивых вычислений")
        print("14. Сгенерировать новые книги")
        print("0. Выход")

        choice = check_choice("Ваш выбор: ", list(range(0, 15)))

        try:
            if choice == 1:
                show_all(books)
            elif choice == 2:
                demo_filter_by_rating(books)
            elif choice == 3:
                demo_get_titles(books)
            elif choice == 4:
                demo_sort_by_pages(books)
            elif choice == 5:
                demo_find_largest(books)
            elif choice == 6:
                demo_has_author(books)
            elif choice == 7:
                demo_generator_period(books)
            elif choice == 8:
                demo_iterator(books)
            elif choice == 9:
                demo_filtered_iterator(books)
            elif choice == 10:
                demo_higher_order(books)
            elif choice == 11:
                demo_comprehensions(books)
            elif choice == 12:
                demo_statistics(books)
            elif choice == 13:
                demonstrate_laziness()
            elif choice == 14:
                count = check_int("Сколько книг создать? ", 1, 30)
                books = generate_random_books(count)
                print(f"Создано {len(books)} книг.")
            elif choice == 0:
                break
        except BookNotFoundError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()