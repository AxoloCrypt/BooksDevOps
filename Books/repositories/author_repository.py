from models import Author
from . import Repository


class AuthorRepository(Repository):

    def __init__(self, context, model=Author):
        super().__init__(context, model)

    
    def get_all_authors(self) -> list[Author] | None:
        return super().get_all()

    
    def get_author_by_id(self, id: int) -> Author | None:
        return super().get_by_id(id)


    def create_author(self, book: Author) -> Author | None:
        created_author = super().create(book)

        if created_author is not None:
            super().save()

        return created_author
    
