from utils.mongo import Mongo


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


def run(data, account):
    account_model = AccountModel()
    post_model = PostModel()
    old_post_model = OldPostModel()
    post_codes = []
    for d in data:
        a = old_post_model.find_one({"providerId": d["providerId"]})
        b = post_model.find_one({"providerId": d["providerId"]})
        if (not a) and (not b):
            post_codes.append(d["code"])
            post_model.insert_one(d)
    account_model.update_upsert({"accountProviderId": account["accountProviderId"]}, {"$set": account})
    return post_codes
