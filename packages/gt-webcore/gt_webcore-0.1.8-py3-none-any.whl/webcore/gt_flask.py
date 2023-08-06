# coding:utf-8
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from .result import Result
from .api_encoder import ApiEncoder
from .error_handler import init_error_handler
from .interceptor import init_interceptor

class GtFlask(Flask):
    def make_response(self, rv):
        if isinstance(rv, Result):
            return super().make_response(jsonify(rv))
        return super().make_response(rv)

    def init_app(self):
        CORS(self, resources={r'/*': {"origins": '*'}})
        self.json_encoder = ApiEncoder
        init_error_handler(self)
        init_interceptor(self)
        
    def register_encoder(self, encoder):
        self.json_encoder.add_encoder(encoder)

    def unregister_encoder(self, encoder):
        self.json_encoder.remove_encoder(encoder)