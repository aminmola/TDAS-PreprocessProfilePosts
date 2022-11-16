from utils.mongo import Mongo


class PostModel(Mongo):
    _connection_name = 'mongo_connection1'
    _collection_name = 'post'
    _db_name = 'data_pipline'


def run(data):
    post_model = PostModel()
    for d in data:
        post_model.insert_one(d)

# def run(data):
#     post_model = PostModel()
#     for d in data:
#         post_model.update_upsert({'_id': d[1]},
#                                  {'$set': {"cleaned_caption": d[0]}})


