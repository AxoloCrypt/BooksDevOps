from sqlalchemy.exc import SQLAlchemyError
from flask_sqlalchemy import SQLAlchemy

class Repository():

    def __init__(self, context: SQLAlchemy, model: object):
        self.context = context
        self.model = model


    def get_all(self) -> list[object] | None:

        try:
            objects = self.context.session.query(self.model).all()
            
            return objects
        except SQLAlchemyError:
            return None


    def get_by_id(self, id: int) -> object | None:

        try:
            object_to_find = self.context.session.query(self.model).get(id)
            
            return object_to_find
        except SQLAlchemyError:
            return None


    def create(self, new_object: object) -> object | None:

        try:
            self.context.session.add(new_object)
            self.context.session.flush()
            
            return new_object
        except SQLAlchemyError:
            return None


    def edit(self, id: int, new_object: object) -> bool:

        object_to_edit = self.get_by_id(id)

        if object_to_edit is None:
            return False
        
        try:

            for attribute, value in new_object.__dict__.items():
                if not attribute.startswith('_'):
                    setattr(object_to_edit, attribute, value)

            self.context.session.flush()

            return True
        except SQLAlchemyError:
            return False
        


    def delete(self, id: int) -> bool:

        object_to_delete = self.get_by_id(id)

        if object_to_delete is None:
            return False
        
        try:
            self.context.session.delete(object_to_delete)
            self.context.session.flush()
            return True
        except SQLAlchemyError:
            return False


    def save(self):
        self.context.session.commit()
