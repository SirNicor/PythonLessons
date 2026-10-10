import sys


def books_by_period(books, start_year, end_year):
    for book in books:
        if start_year <= book.year <= end_year:
            yield book


def books_by_author(books, author_name):
    for book in books:
        if book.author.lower() == author_name.lower():
            yield book


def high_rated_books(books, min_rating):
    for book in books:
        if book.rating >= min_rating:
            yield book


def large_books(books, min_pages):
    for book in books:
        if book.number_of_pages >= min_pages:
            yield book


def demonstrate_laziness():
    print("=== Демонстрация ленивых вычислений ===\n")
    
    list_result = [x * x for x in range(1_000_000)]
    list_size = sys.getsizeof(list_result)
    print(f"Список из 1 000 000 элементов:")
    print(f"  Размер в памяти: {list_size} байт ({list_size / 1024 / 1024:.2f} МБ)")
    print(f"  Значения вычислены: сразу все")
    print(f"  Первый элемент: {list_result[0]}, последний: {list_result[-1]}")
    
    gen_result = (x * x for x in range(1_000_000))
    gen_size = sys.getsizeof(gen_result)
    print(f"\nГенератор из 1 000 000 элементов:")
    print(f"  Размер в памяти: {gen_size} байт")
    print(f"  Значения вычисляются: по мере запроса (лениво)")
    
    first_five = [next(gen_result) for _ in range(5)]
    print(f"  Первые 5 значений: {first_five}")
    print(f"  Остальные ещё не вычислены!")


class BookIterator:
    
    def __init__(self, books):
        self.books = books
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.books):
            raise StopIteration
        
        result = self.books[self.index]
        self.index += 1
        return result


class FilteredBookIterator:
    
    def __init__(self, books, min_rating=0):
        self.books = books
        self.index = 0
        self.min_rating = min_rating

    def __iter__(self):
        return self

    def __next__(self):
        while self.index < len(self.books):
            book = self.books[self.index]
            self.index += 1
            if book.rating >= self.min_rating:
                return book
        raise StopIteration