from . import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


    def __str__(self):
        return f'{{ "id": {self.id}, "name": "{self.name}" }}'