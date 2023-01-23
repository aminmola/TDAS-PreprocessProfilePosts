from utils.mongo import Mongo


class PostModel(Mongo):
    _connection_name = 'mongo_connection1'
    _collection_name = 'post'
    _db_name = 'data_pipline'


class AccountModel(Mongo):
    _connection_name = 'mongo_connection1'
    _collection_name = 'accounts'
    _db_name = 'data_pipline'


def run(data, account):
    account_model = AccountModel()
    post_model = PostModel()
    for d in data:
        post_model.insert_one(d)
    account_model.update_upsert({"accountProviderId": account["accountProviderId"]}, {"$set":account})
