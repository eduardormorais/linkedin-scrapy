from flask_restful import Resource, Api
from flask import Flask, request
from subproces_webhook import SubprocesWebHook
from resultsearch_webhook import ResultSearchWebHook
import json

app = Flask(__name__)
api = Api(app)

api.add_resource(SubprocesWebHook, '/api/pessoas/')
api.add_resource(ResultSearchWebHook, '/api/resultsearch/')

if __name__ == '__main__':
    app.run(host= '0.0.0.0')
