from controllers.book import Book
from models.external_book_data import BookService


class BookAdapter:
    def __init__(self, service: BookService):
        self.service = service

    def fetch_book(self, isbn: str) -> Book | None:
        data = self.service.get_book_by_isbn(isbn)

        if data is None:
            return None

        return Book(
            title=data.get("title", ""),
            author=data.get("author", ""),
            isbn=isbn,
            description=data.get("description", ""),
            genre=data.get("genre", ""),
            published_year=data.get("published_year"),
        )
