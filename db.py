from flask import current_app, g
from werkzeug.local import LocalProxy

from datetime import datetime
from pymongo import MongoClient, DESCENDING, ASCENDING
from bson import ObjectId


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)
    DB_URI = "mongodb://localhost:27017"
    DB_NAME = "autoCompletionApp"
    if db is None:
        db = g._database = MongoClient(
            DB_URI,
            maxPoolSize=50,
            wTimeoutMS=2500
        )[DB_NAME]
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def get_model(model_id: str):
    result = db.models.find_one({'_id': ObjectId(model_id)})
    return result


def add_model(model_name: str):
    model_doc = {
        'name': model_name,
        'createDate': datetime.utcnow()
    }
    return db.models.insert_one(model_doc)
