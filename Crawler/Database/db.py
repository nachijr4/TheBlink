from pymongo import MongoClient
import datetime

class DB:
    db = MongoClient().TheBlink

    def insert_one(self, collection, data):
        data['created_at'] = datetime.datetime.utcnow()
        data['updated_at'] = datetime.datetime.utcnow()
        DB.db[collection].insert_one(data)

    def insert_many(self, collection, datas):
        for data in datas:
            data['created_at'] = datetime.datetime.utcnow()
            data['updated_at'] = datetime.datetime.utcnow()
        
        try:
            DB.db[collection].insert_many(datas)
            return True
        except:
            return False

# test = DB()

# post = {"author": "Mike",
#         "text": "My first blog post!",
#        "tags": ["mongodb", "python", "pymongo"],
#         "date": datetime.datetime.utcnow()}

# test.insert_one('collected_page', post)