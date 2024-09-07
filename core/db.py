import pymongo

class MongoDB:
    def __init__(self, host: str, port: int, db_name: str, collection_name: str,username=None, password=None):
        uri = f"mongodb://{username}:{password}@{host}:{port}/" if username and password else f"mongodb://{host}:{port}/"
        self.client = pymongo.MongoClient(uri)
        self.collection_name = collection_name
        self.db = self.client[db_name]
    def list_all_collections(self):
        return self.db.list_collection_names()
    def get_collection(self,collection_name):
        return self.db[collection_name]
    async def insert_one(self, data):
        collection = self.get_collection(self.collection_name)
        result = collection.insert_one(data)
        return result.inserted_id

    def find_all(self):
        collection = self.get_collection(self.collection_name)
        return list(collection.find())
    def update_one(self, query, update):
        collection = self.get_collection(self.collection_name)
        return collection.update_one(query, update)
    def find_one(self, query):
        collection = self.get_collection(self.collection_name)
        return collection.find_one(query)