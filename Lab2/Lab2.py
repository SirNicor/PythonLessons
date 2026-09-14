import random

def main():
    while True:
        books = []
        print("Проверка на случайных данных - 1, ввод собственных данных - 2")
        change = checkTryCatch()
        if change == 1:
            numberBooks = random.randint(3, 15)
            input(f"Количество книг: {numberBooks}")
            titles = ["Война и мир", "Преступление и наказание", "Мастер и Маргарита",
                       "Евгений Онегин", "Мёртвые души", "Отцы и дети", "Герой нашего времени",
                       "Идиот", "Братья Карамазовы", "Анна Каренина", "Тихий Дон",
                       "Доктор Живаго", "1984", "451 градус по Фаренгейту", "Дюна"]
            authors = ["Толстой", "Достоевский", "Булгаков", "Пушкин", "Гоголь",
                        "Тургенев", "Лермонтов", "Брэдбери", "Оруэлл", "Герберт"]
            for i in range(numberBooks):
                title = random.choice(titles) + f" ({i+1})"
                author = random.choice(authors)
                year = random.randint(1800, 2025)
                pages = random.randint(50, 1500)
                book = {"title": title, "author": author, "year": year, "pages": pages}
                books.append(book)
                print(f"Книга: {title}, автор: {author}, год: {year}, страниц: {pages}")
        else:
            numberBooks = int(input("Введите количество книг на ввод: "))
            print("Вводите данные через пробел: название автор год количество_страниц")
            for i in range(numberBooks):
                while True:
                    try:
                        raw = input(f"Книга {i+1}: ").split()
                        if len(raw) < 4:
                            raise IndexError
                        title = raw[0]
                        author = raw[1]
                        year = int(raw[2])
                        pages = int(raw[3])
                        if year < 1 or pages < 1:
                            raise ValueError
                    except (ValueError, IndexError):
                        print("Неверный формат. Пример: Название Автор 2020 350")
                    else:
                        break
                book = {"title": title, "author": author, "year": year, "pages": pages}
                books.append(book)
    
        # ===== МЕНЮ =====
        while True:
            print("\n===== МЕНЮ =====")
            print("1. Добавить книгу")
            print("2. Показать все книги")
            print("3. Поиск по автору")
            print("4. Фильтрация по году")
            print("5. Сортировка по страницам")
            print("6. Статистика")
            print("7. Уникальные авторы")
            print("8. Удалить книгу")
            print("0. Выход")
            choice = checkMenuChoice()

            if choice == 1:
                add_book(books)
            elif choice == 2:
                show_books(books)
            elif choice == 3:
                search_by_author(books)
            elif choice == 4:
                filter_by_year(books)
            elif choice == 5:
                sort_by_pages(books)
            elif choice == 6:
                show_statistics(books)
            elif choice == 7:
                show_unique_authors(books)
            elif choice == 8:
                delete_book(books)
            elif choice == 0:
                break

        print("Если вы хотите повторить программу введите 1, иначе 2")
        change = checkTryCatch()
        if change == 2:
            break


def add_book(books):
    while True:
        try:
            raw = input("Введите данные (название автор год страницы): ").split()
            if len(raw) < 4:
                raise IndexError
            title = raw[0]
            author = raw[1]
            year = int(raw[2])
            pages = int(raw[3])
            if year < 1 or pages < 1:
                raise ValueError
        except (ValueError, IndexError):
            print("Неверный формат. Пример: Название Автор 2020 350")
        else:
            break
    book = {"title": title, "author": author, "year": year, "pages": pages}
    books.append(book)
    print(f"Книга '{title}' добавлена.")


def show_books(books):
    if len(books) == 0:
        print("Список книг пуст.")
        return
    for i, book in enumerate(books):
        print(f"{i+1}. {book['title']} | {book['author']} | {book['year']} | {book['pages']} стр.")


def search_by_author(books):
    author = input("Введите автора для поиска: ")
    found = [book for book in books if book["author"].lower() == author.lower()]
    if len(found) == 0:
        print(f"Книги автора '{author}' не найдены.")
    else:
        print(f"Найдено книг: {len(found)}")
        for book in found:
            print(f"  {book['title']} | {book['year']} | {book['pages']} стр.")


def filter_by_year(books):
    while True:
        try:
            year = int(input("Показать книги после года: "))
        except ValueError:
            print("Введите целое число.")
        else:
            break
    filtered = [book for book in books if book["year"] > year]
    if len(filtered) == 0:
        print(f"Книг после {year} года не найдено.")
    else:
        print(f"Книг после {year} года: {len(filtered)}")
        for book in filtered:
            print(f"  {book['title']} | {book['author']} | {book['year']} | {book['pages']} стр.")


def sort_by_pages(books):
    if len(books) == 0:
        print("Список книг пуст.")
        return
    sorted_books = sorted(books, key=lambda b: b["pages"])
    print("Книги отсортированы по количеству страниц (по возрастанию):")
    for book in sorted_books:
        print(f"  {book['title']} | {book['pages']} стр.")


def show_statistics(books):
    if len(books) == 0:
        print("Список книг пуст.")
        return
    pages_list = [book["pages"] for book in books]
    avg_pages = sum(pages_list) / len(pages_list)
    max_pages = max(pages_list)
    min_pages = min(pages_list)
    thickest = [book for book in books if book["pages"] == max_pages][0]
    input(f"""Средняя толщина книги: {avg_pages:.1f} стр.
Максимум страниц: {max_pages} ('{thickest['title']}')
Минимум страниц: {min_pages}
Всего книг: {len(books)}""")


def show_unique_authors(books):
    if len(books) == 0:
        print("Список книг пуст.")
        return
    unique_authors = set(book["author"] for book in books)
    print(f"Уникальных авторов: {len(unique_authors)}")
    for author in unique_authors:
        print(f"  {author}")


def delete_book(books):
    if len(books) == 0:
        print("Список книг пуст.")
        return
    show_books(books)
    while True:
        try:
            index = int(input("Введите номер книги для удаления: "))
            if index < 1 or index > len(books):
                raise IndexError
        except ValueError:
            print("Введите целое число.")
        except IndexError:
            print(f"Номер должен быть от 1 до {len(books)}.")
        else:
            break
    removed = books.pop(index - 1)
    print(f"Книга '{removed['title']}' удалена.")


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


if __name__ == "__main__":
    main()