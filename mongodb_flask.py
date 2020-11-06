from flask import request
from flask_api import FlaskAPI, status

from mongodb_api import MongoAPI

app = FlaskAPI(__name__)
mongo = MongoAPI()


@app.route('/')
def base():
    return {"Status": "API is UP"}, status.HTTP_200_OK


@app.route('/mongodb', methods=['GET'])
def mongo_read():
    data = None
    try:
        data = request.get_json(force=True)
        title = data['title']
    except KeyError as ex:
        return 'Invalid field ' + str(ex), status.HTTP_400_BAD_REQUEST
    except Exception as ex:
        return 'Invalid body', status.HTTP_400_BAD_REQUEST

    response = mongo.read(data)
    if response:
        return response, status.HTTP_200_OK
    return 'Not found', status.HTTP_404_NOT_FOUND


@app.route('/mongodb', methods=['POST'])
def mongo_write():
    data = None
    try:
        data = request.get_json(force=True)
        title = data['title']
        text = data['text']
        author = data['author']
    except KeyError as ex:
        return 'Invalid field ' + str(ex), status.HTTP_400_BAD_REQUEST
    except Exception as ex:
        return 'Invalid body', status.HTTP_400_BAD_REQUEST

    if mongo.write(data):
        return 'Inserted', status.HTTP_201_CREATED
    return 'Error write', status.HTTP_400_BAD_REQUEST


@app.route('/mongodb', methods=['PUT'])
def mongo_update():
    try:
        data = request.get_json(force=True)
        title = data['title']
    except KeyError as ex:
        return 'Invalid field ' + str(ex), status.HTTP_400_BAD_REQUEST
    except Exception as ex:
        return 'Invalid body', status.HTTP_400_BAD_REQUEST

    if mongo.update(data):
        return 'Updated', status.HTTP_200_OK
    return 'Not found', status.HTTP_404_NOT_FOUND


@app.route('/mongodb', methods=['DELETE'])
def mongo_delete():
    data = request.json
    if data is None or data == {}:
        return 'Invalid body', status.HTTP_400_BAD_REQUEST
    if mongo.delete(data):
        return 'Deleted', status.HTTP_200_OK
    return 'Not found', status.HTTP_404_NOT_FOUND


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
