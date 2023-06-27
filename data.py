from utils.mongo import Mongo
from datetime import datetime


class PostModel(Mongo):
    _connection_name = 'mongo_connection1'
    _collection_name = 'post'
    _db_name = 'data_pipline'


class OldPostModel(Mongo):
    _connection_name = 'mongo_connection1'
    _collection_name = 'old_posts'
    _db_name = 'data_pipline'


class AccountModel(Mongo):
    _connection_name = 'mongo_connection1'
    _collection_name = 'accounts'
    _db_name = 'data_pipline'


out = []
post_model = PostModel()
query = {
    "$and": [{'local_created_at': {"$gt": datetime.strptime('2023-02-18T00:00:00.0000000', '%Y-%m-%dT%H:%M:%S.0000000')}},
             {'local_created_at': {"$lt": datetime.strptime('2023-02-19T00:00:00.0000000', '%Y-%m-%dT%H:%M:%S.0000000')}}
             ]}
posts = post_model.collection.find(query, {"code": "$code"})
for doc in posts:
    out.append(doc)

