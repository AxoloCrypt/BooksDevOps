from flask import Blueprint, g, current_app, jsonify, Response, request
from repositories import AuthorRepository
from models import db, Author
from flask_restx import Resource, fields, Namespace

authors_blueprint = Namespace('authors')

author_model = authors_blueprint.model('Author', {
    'id': fields.Integer(readonly=False, description='Author unique identifier'),
    'name': fields.String(required=True, description='Author name')
})


@authors_blueprint.route('/authors')
class AuthorsResource(Resource):
    @authors_blueprint.doc('get_authors')
    def get(self):

        authors = g.author_repository.get_all()

        if authors is None:
            return jsonify({
                'error': 'A server error occurred. Please try again later.',
                'message': 'Something went wrong while searching for authors'
            }), 500

        json_strings = [author.__str__() for author in authors]

        json_array = "[" + ",".join(json_strings) + "]"

        return Response(json_array, content_type="application/json")


    @authors_blueprint.expect(author_model)
    @authors_blueprint.doc('create_author')
    def post(self):

        author_json = request.get_json()

        if author_json is None:
            abort(400)
            return jsonify({
                'error': 'Bad request',
                'message': 'Invalid format for creating an author'
            }), 400

        
        new_author = Author()
        new_author.name = author_json.get('name')

        with current_app.app_context():
            g.author_repository = AuthorRepository(db)

            created_author = g.author_repository.create_author(new_author)

            if created_author is None:
                return jsonify({
                    'error': 'A server error occurred. Please try again later.',
                    'message': 'Something went wrong while creating the author'
                }), 500

            g.author_repository.save()

            new_author_json = str(created_author)

        return Response(new_author_json, content_type="application/json") 

