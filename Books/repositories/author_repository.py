from models import Author
from . import Repository


class AuthorRepository(Repository):

    def __init__(self, context, model=Author):
        super().__init__(context, model)


    def create_author(self, book: Author) -> Author | None:
        created_author = super().create(book)

        if created_author is not None:
            super().save()

        return created_author
    
