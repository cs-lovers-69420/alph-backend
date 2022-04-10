# This file contains the specifications for the API used in Project Alph.
# API details:
# 1) Endpoints: /pool

from flask import Flask
from flask_restful import Resource, Api, reqparse

APP = Flask(__name__)
API = Api(APP)


class Pool(Resource):
    def get(self):
        return("hello there")


API.add_resource(Pool, "/pool")
if __name__ == '__main__':
    APP.run()
