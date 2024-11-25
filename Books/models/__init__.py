from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .author import Author
from .book import Book
