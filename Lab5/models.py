from abc import ABC, abstractmethod


class Book(ABC):
    
    def __init__(self, title, author, year, number_of_pages, rating):
        self.title = title
        self.author = author
        self.year = year
        self.number_of_pages = number_of_pages
        self.rating = rating

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not (0 <= value <= 100):
            raise ValueError("Рейтинг должен быть от 0 до 100")
        self._rating = value

    @property
    def number_of_pages(self):
        return self._number_of_pages

    @number_of_pages.setter
    def number_of_pages(self, value):
        if value <= 0:
            raise ValueError("Количество страниц должно быть положительным")
        self._number_of_pages = value

    @abstractmethod
    def get_category(self):
        pass

    def __str__(self):
        return (f"[{self.title}] {self.author} | {self.year} г. | "
                f"{self.number_of_pages} стр. | Рейтинг: {self.rating}")

    def __lt__(self, other):
        return self.number_of_pages < other.number_of_pages

    def __eq__(self, other):
        return (self.title == other.title and 
                self.author == other.author)


class FictionBook(Book):
    
    def get_category(self):
        return "Художественная"

    def __str__(self):
        return f"{super().__str__()} | Категория: {self.get_category()}"


class NonFictionBook(Book):
    
    def __init__(self, title, author, year, number_of_pages, rating, subject):
        super().__init__(title, author, year, number_of_pages, rating)
        self.subject = subject

    def get_category(self):
        return f"Научная ({self.subject})"

    def __str__(self):
        return f"{super().__str__()} | Категория: {self.get_category()}"


class BookNotFoundError(Exception):
    pass