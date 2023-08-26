import uuid 
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from db import db

from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import StoreSchema


#Create a flask_smorest blue print object 
blp = Blueprint("Stores", "store", description="Operaions on stores")


#Inherit class from MethodView and decorate the class with endpoint route
@blp.route("/store/<int:store_id>")
class Item(MethodView):
# def the endpoint methods
# get_store
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store


# delete store
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}


@blp.route("/store")
class StoreList(MethodView):
    # get all stores
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    

    # create a store
    @blp.arguments(StoreSchema)
    @blp.response(200,StoreSchema)
    def post(self, store_data):

        store = StoreModel(**store_data)       # Item model will check the required fields

        try:
            db.session.add(store)
            db.session.commit()             # write to disk
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occur while inserting the store.")

        return store, 201 # accepted the request