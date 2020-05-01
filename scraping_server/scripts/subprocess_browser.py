 
import os
import subprocess
import json
from flask_restful import Resource
from flask import request
import uuid

# Example post: http://localhost:5000/api/pessoas/?valueSearch=Brasilia

class SubprocessWebHook(Resource):
    def post(self):
        try:
<<<<<<< HEAD
            value_search = dict(cargo = request.form.get('cargo'),
                                localidade = request.form.get('localidade'),
                                setores = request.form.getlist('setores'))
=======
            value_search = dict(cargo = str(request.form['cargo']),
                                localidade = str(request.form['localidade']),
                                qtd = int(request.form['qtd']),                                
                                setores = list(request.form.getlist('setores')))
>>>>>>> 8b1614401e3d9a68d35d01d162c34b5634498f04
            print("Dados de pesquisa recebidos: {}".format(value_search))
            file_name = f"request-{uuid.uuid4().hex}.json"
            self.startSubprocess(f"python3.6 linkedin_spider.py --v '{json.dumps(value_search)}' --o {file_name}")
            return file_name
        except Exception as excs:
            print(excs)
            return 504

    def startSubprocess(self, command):
        subprocess.Popen(args=command, 
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, shell=True)