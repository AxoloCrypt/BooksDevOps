from flask import Flask, g
from flask_migrate import Migrate
from flask_restx import Api
from models import db
from routes import books_blueprint, authors_blueprint
from dotenv import load_dotenv
from repositories import BookRepository, AuthorRepository
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db.init_app(app)
migrate = Migrate(app, db)

api = Api(app, version='0.1', title='Books API')

api.add_namespace(books_blueprint, path='/api/v1')
api.add_namespace(authors_blueprint, path='/api/v1')

@app.before_request
def init_repositories():
    g.book_repository = BookRepository(context=db)
    g.author_repository = AuthorRepository(context=db)

"""
Test with powersheell:
Get books:  Invoke-WebRequest -Method GET -Uri "http://localhost:5000/api/books"
Get book by id: Invoke-WebRequest -Method GET -Uri "http://localhost:5000/api/books/<<id>>"
Create book: Invoke-WebRequest -Method POST -Uri "http://localhost:5000/api/books" -Body '{ "title": "Mountains of madness", "author_id": 10, "publication_year":"1930"}' -ContentType "application/json"
Edit book: Invoke-WebRequest -Method PUT -Uri "http://localhost:5000/api/books" -Body '{ "id": 1, "title": "Mountains", "author_id": 10, "publication_year":"1929"}' -ContentType "application/json" 
Delete book: Invoke-WebRequest -Method DELETE -Uri "http://localhost:5000/api/books/<<id>>"
Get authors:  Invoke-WebRequest -Method GET -Uri "http://localhost:5000/api/authors"
Create author: Invoke-WebRequest -Method POST -Uri "http://localhost:5000/api/authors" -Body '{ "name": "Tolkien"}' -ContentType "application/json"
"""
if __name__ == '__main__':
    app.run(debug=True, port=5000)
