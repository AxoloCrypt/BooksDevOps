from flask import Blueprint, g, current_app, Response, request, jsonify
from flask_restx import Resource, fields, Namespace
from models import db, Book
from repositories import BookRepository

books_blueprint = Namespace('books')

book_model = books_blueprint.model('Book', {
    'id': fields.Integer(readonly=True, description='The book unique identifier'),
    'author_id': fields.Integer(required=True, description='The author identifier'),
    'title': fields.String(required=True, description='The title of the book'),
    'publication_year': fields.Integer(required=True, description='The publication year of the book')
})


@books_blueprint.route('/books')
class Books(Resource):
    @books_blueprint.doc('get_books')
    def get(self):
        books = g.book_repository.get_all()

        if books is None:
            return jsonify({
                'error': 'A server error occurred. Please try again later.',
                'message': 'Something went wrong while searching for books'
            }), 500

        json_strings = [str(book) for book in books]

        json_array = "[" + ",".join(json_strings) + "]"

        return Response(json_array, content_type="application/json")

    @books_blueprint.expect(book_model)
    @books_blueprint.doc('create_book')
    def post(self):

        book_json = request.get_json()

        if book_json is None:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Invalid book format'
            }), 400

        new_book = Book()
        new_book.author_id = book_json.get('author_id')
        new_book.title = book_json.get('title')
        new_book.publication_year = book_json.get('publication_year')
        
        with current_app.app_context():
            g.book_repository = BookRepository(db)

            created_book = g.book_repository.create_book(new_book)

            if created_book is None:
                return jsonify({
                    'error': 'A server error occurred. Please try again later.',
                    'message': 'Something went wrong while creating the books'
                }), 500

            created_book_json = str(created_book)

        return Response(created_book_json, content_type='application/json')


    @books_blueprint.expect(book_model)
    @books_blueprint.doc('update_book')
    def put(self):

        book_json = request.get_json()

        if book_json is None:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Invalid book format'
            }), 400

        book = Book()
        book.id = book_json.get('id')
        book.author_id = book_json.get('author_id')
        book.title = book_json.get('title')
        book.publication_year = book_json.get('publication_year')
        
        with current_app.app_context():
            g.book_repository = BookRepository(db)

            is_book_updated = g.book_repository.edit_book(book.id, book)

        if not is_book_updated:
            return jsonify({
                'error': 'A server error occurred. Please try again later.',
                'message': 'Something went wrong while updating the book'
            }), 500

        return 'Book was updated sucessfully', 200


@books_blueprint.route('/books/<int:id>')
class BookResources(Resource):

    @books_blueprint.doc('get_book_by_id')    
    def get(self,id):

        book = g.book_repository.get_by_id(id)

        if book is None:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Invalid book format'
            }), 400


        json_string = str(book)

        return Response(json_string, content_type="application/json")

    @books_blueprint.doc('delete_book')
    def delete(self, id):

        with current_app.app_context():
            g.book_repository = BookRepository(db)

            is_book_deleted = g.book_repository.delete_book(id)

        if not is_book_deleted:
            return jsonify({
                'error': 'A server error occurred. Please try again later.',
                'message': 'Something went wrong while deleting the book'
            }), 500

        return 'Book was deleted', 200

