
import json
from bottle import route, run, get, put, request, abort, response, default_app
from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.mydatabase

@put('/documents')
def put_document():
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('_id'):
        abort(400, 'No _id specified')
    try:
        db['documents'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

@get('/documents/<id>')
def get_document(id):
    entity = db['documents'].find_one({'_id':id})
    if not entity:
        abort(404, 'No document with id %s' % id)
    return entity

@route('/')
def index():
    return "hi, welcome to katlis.com"

if __name__ == "__main__":
    run(host="localhost", port=8081)
else:
    application = default_app()