from pymongo import MongoClient


class MongoAPI:
    def __init__(self):
        # self.client = MongoClient('mongodb://localhost:5000/') -- local testing
        self.client = MongoClient('mongodb://mymongo_1:27017/')
        cursor = self.client['test']
        self.collection = cursor['news']

    def read(self, data):
        title = data.get('title')
        documents = [self.collection.find_one({'title': title})]
        output = []
        if documents[0] is not None:
            output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def write(self, data):
        response = self.collection.insert_one(data)
        return response.inserted_id

    def update(self, data):
        title = data['title']
        update = {}
        if data.get('text'):
            update['text'] = data.get('text')
        if data.get('author'):
            update['author'] = data.get('author')
        updated_data = {"$set": update}
        response = self.collection.update_one({'title': title}, updated_data)
        return response.modified_count

    def delete(self, data):
        response = self.collection.delete_one(data)
        return response.deleted_count
