from models import Book
from . import Repository


class BookRepository(Repository):

    def __init__(self, context, model=Book):
        super().__init__(context, model)

    
    def get_all_books(self) -> list[Book] | None:
        return super().get_all()

    
    def get_book_by_id(self, id: int) -> Book | None:
        return super().get_by_id(id)


    def create_book(self, book: Book) -> Book | None:
        created_book = super().create(book)

        if created_book is not None:
            super().save()

        return created_book

    
    def edit_book(self, id: int, new_book: Book) -> bool:

        is_book_edited = super().edit(id, new_book)

        if is_book_edited:
            super().save()

        return is_book_edited

    
    def delete_book(self, id: int) -> bool:
        is_book_deleted = super().delete(id)

        if is_book_deleted:
            super().save()

        return is_book_deleted
