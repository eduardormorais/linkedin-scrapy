from flask_restful import Resource, Api
import time
from selenium import webdriver
from flask import Flask, request
from os import path
from resultsearch_webhook import ResultSearchWebHook
from linkedin_selenium import LinkedinSelenium
from subprocess_browser import SubprocessWebHook
from setores_webhook import SetoresWebHook
import json, os

app = Flask(__name__)
api = Api(app)
if path.exists('cookies.json') is not True:
    print('Realizando login para salvar os cookies.')
    linkedin_selenium = LinkedinSelenium()
    chrome_driver = webdriver.Chrome(executable_path=linkedin_selenium.chrome_driver_path)
    linkedin_selenium.sign_in(chrome_driver)
    linkedin_selenium.save_session_cookies(chrome_driver)
    chrome_driver.close()

api.add_resource(ResultSearchWebHook, '/api/resultado/')
api.add_resource(SubprocessWebHook, '/api/pesquisa/')
api.add_resource(SetoresWebHook, '/api/setores/')


if __name__ == '__main__':
    app.run(host= '0.0.0.0')