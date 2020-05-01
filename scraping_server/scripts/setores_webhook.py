from flask_restful import Resource
import json
import os

# Example post: http://localhost:5000/api/setores

class SetoresWebHook(Resource):
    
    def get(self):
        try:
            f = open("ids_setores.json", "r")
            setores = f.read()
            return json.loads(setores)
        except Exception as e:
            print(e) 
            return 504
    