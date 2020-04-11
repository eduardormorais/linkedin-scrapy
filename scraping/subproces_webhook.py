import os
import subprocess
from flask_restful import Resource
from flask import request
import uuid

os.environ['EMAIL'] = "email@gmail.com"
os.environ['PASSWORD'] = "senha"

# Example post: http://localhost:5000/api/pessoas/?valueSearch=Brasilia

class SubprocesWebHook(Resource):

    def post(self):
        try:
            value_search = request.args.get('valueSearch')
            file_name = f"request-{uuid.uuid4().hex}.json"
            print(value_search)   
            self.startSubprocess(f"scrapy runspider scraping.py -a value_search={value_search} -a email={os.environ['EMAIL']} -a password={os.environ['PASSWORD']} -a output_file={file_name}")
            return file_name
        except:
            return 504

    def startSubprocess(self, command):
        subprocess.Popen(args=command, 
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
