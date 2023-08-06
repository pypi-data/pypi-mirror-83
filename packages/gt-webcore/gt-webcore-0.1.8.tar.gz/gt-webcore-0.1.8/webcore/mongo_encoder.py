# -*- coding: utf-8 -
from flask.json import JSONEncoder 
from bson.objectid import ObjectId
from pymongo.cursor import Cursor

class MongoEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, Cursor):
            return list(obj)
            
        return None