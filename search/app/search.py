from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class SearchSimple(Resource):
    def get(self, search_keyword):
        return {todo_id: todos[todo_id]}

api.add_resource(SearchSimple, '/<string:search_keyword>')

if __name__ == '__main__':
    app.run(debug=True)
