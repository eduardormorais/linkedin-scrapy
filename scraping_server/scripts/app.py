from flask_restful import Resource, Api
import time
from selenium import webdriver
from flask import Flask, request
from os import path
from flask_cors import CORS
from resultsearch_webhook import ResultSearchWebHook
from linkedin_selenium import LinkedinSelenium
from subprocess_browser import SubprocessWebHook
from setores_webhook import SetoresWebHook
import json, os

app = Flask(__name__)
CORS(app)
api = Api(app)
linkedin_selenium = LinkedinSelenium()
api.add_resource(ResultSearchWebHook, '/api/resultado/')
api.add_resource(SubprocessWebHook, '/api/pesquisa/')
api.add_resource(SetoresWebHook, '/api/setores/')

@app.route('/', methods=['GET'])
def health_check():
    return 'application is running...'

@app.route('/login', methods=['POST'])
def sign_up():
    linkedin_selenium.initialize_driver()
    status = linkedin_selenium.is_authenticated()
    return str(status)

@app.route('/set_code', methods=['POST'])
def receive_user_code():
    linkedin_selenium.set_code(request.form.get('code'))
    return 200


port = os.environ.get('PORT', 5000)
if __name__ == '__main__':
    app.run(host= '0.0.0.0',port=port, debug=True)