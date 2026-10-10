from functools import reduce


def filter_objects(objects, predicate):
    return list(filter(predicate, objects))


def transform_objects(objects, operation):
    return list(map(operation, objects))


def sort_objects(objects, key_function, reverse=False):
    return sorted(objects, key=key_function, reverse=reverse)


def reduce_objects(objects, operation, initializer=None):
    if initializer is not None:
        return reduce(operation, objects, initializer)
    return reduce(operation, objects)


def get_titles(books):
    return list(map(lambda book: book.title, books))


def get_authors(books):
    return [book.author for book in books]


def filter_by_rating(books, min_rating):
    return list(filter(lambda book: book.rating >= min_rating, books))


def filter_by_year_range(books, start_year, end_year):
    return [book for book in books if start_year <= book.year <= end_year]


def sort_by_pages(books):
    return sorted(books, key=lambda book: book.number_of_pages)


def sort_by_rating_desc(books):
    return sorted(books, key=lambda book: book.rating, reverse=True)


def find_largest_book(books):
    if not books:
        return None
    return reduce(
        lambda a, b: a if a.number_of_pages > b.number_of_pages else b,
        books
    )


def get_total_pages(books):
    return reduce(lambda total, book: total + book.number_of_pages, books, 0)


def get_average_rating(books):
    if not books:
        return 0
    total = reduce(lambda s, book: s + book.rating, books, 0)
    return total / len(books)


def has_author(books, author_name):
    return any(book.author.lower() == author_name.lower() for book in books)


def all_books_above_rating(books, min_rating):
    return all(book.rating >= min_rating for book in books)


def get_books_by_author_dict(books):
    authors = list(set(book.author for book in books))
    return {
        author: [b for b in books if b.author == author]
        for author in authors
    }


def get_unique_authors_set(books):
    return {book.author for book in books}