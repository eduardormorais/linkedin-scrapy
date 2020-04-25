from flask_restful import Resource
from flask import request
import json
import os

# Example post: http://localhost:5000/api/resultsearch/?fileName=request-c5ae3401c99d42fda8c0bec40e4f78cb.txt

class ResultSearchWebHook(Resource):
    
    def get(self):
        try:
            file_name = request.args.get('fileName')
            print(f"File --> {file_name}")
            process_finish = self.finish_file(file_name)
            print(f"Finish --> {process_finish}")
            if(process_finish):
                return self.get_file(file_name)    
            
            return process_finish
        except Exception as e:
            print(e) 
            return 504
    
    def finish_file(self, file_name):
        return os.path.exists(f"files/{file_name}")
    
    def get_file(self, file_name):
        with open(f"files/{file_name}", "r") as arquivo_resultado:
            resultado = json.load(arquivo_resultado)

        return resultado 
              
# if __name__ == "__main__":
#     f = open("files/request-c5ae3401c99d42fda8c0bec40e4f78cb.txt", "r")
#     print(f.read())