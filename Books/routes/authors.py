from flask import Blueprint, g, current_app, abort, Response, request
from repositories import AuthorRepository
from models import db, Author

authors_blueprint = Blueprint('authors', __name__)


@authors_blueprint.before_request
def init_author_repository():
    g.author_repository = AuthorRepository(db)


@authors_blueprint.route('/authors', methods=['GET'])
def get_authors():

    authors = g.author_repository.get_all_authors()

    if authors is None:
        abort(500)

    json_strings = [author.__str__() for author in authors]

    json_array = "[" + ",".join(json_strings) + "]"

    return Response(json_array, content_type="application/json")


@authors_blueprint.route('/authors', methods=['POST'])
def create_author():

    author_json = request.get_json()

    if author_json is None:
        abort(400)

    
    new_author = Author()
    new_author.name = author_json.get('name')

    with current_app.app_context():
        g.author_repository = AuthorRepository(db)

        created_author = g.author_repository.create_author(new_author)

        if create_author is None:
            abort(500)

        g.author_repository.save()

        new_author_json = created_author.__str__()

    return Response(new_author_json, content_type="application/json") 
