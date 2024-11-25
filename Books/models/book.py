from . import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    publication_year = db.Column(db.String(255), nullable=False)


    def __str__(self):
        return f'{{ "id": {self.id}, "title": "{self.title}", "author_id": {self.author_id}, "publication_year": "{self.publication_year}"}}'
