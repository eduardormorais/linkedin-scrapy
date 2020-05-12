 
import os
import subprocess
import json
from flask_restful import Resource
from flask import request
import logging
import uuid
from os import path
from linkedin_selenium import LinkedinSelenium

class SubprocessWebHook(Resource):
    def post(self):
        try:
            value_search = dict(cargo = request.form.get('cargo'),
                                qtd = int(request.form.get('qtd')),
                                localidade = request.form.get('localidade'),
                                setores = request.form.getlist('setores'))
            print("Dados de pesquisa recebidos: {}".format(value_search))
            file_name = f"request-{uuid.uuid4().hex}.json"
            self.startSubprocess(f"python3.6 linkedin_spider.py --v '{json.dumps(value_search)}' --o {file_name}")
            return file_name
        except Exception as excs:
            print(excs)
            return 504

    def startSubprocess(self, command):
        process = subprocess.Popen(args=command, 
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, shell=True)