from utils.mysql import MySQL
# from utils.mongo import Mongo


def run():
    with MySQL(db_name='tathir') as db:
        query = 'SELECT * FROM contents  ' \
                'WHERE is_used=0 ' \
                'ORDER BY created_at DESC  ' \
                'limit 1000;'
        data = db.read(query)
        ids = ''
        when_then = ''
        for d in data:
            ids += f"{d['id']}, "
            when_then += f"WHEN {d['id']} THEN 1 "
        ids = ids[:-2]
        query = f"UPDATE contents " \
                f"SET is_used = ( CASE id {when_then} END) "\
                f"WHERE id in ({ids});"
        db.execute(query)
        # for d in data:
        #     db.update(table='contents', record={'is_used': 1}, condition=f'id={d["id"]}')
    return data
    # data = pd.read_csv(f'{cfg.root_path}/components/contents.csv')
    # data = [json.loads(d.to_json()) for i, d in data.iterrows()]
    #return data


# class PostModel(Mongo):
#     _connection_name = 'mongo_connection1'
#     _collection_name = 'post'
#     _db_name = 'data_pipline'
#
#
# def run():
#     post_model = PostModel()
#     query_1 = {
#         "$or": [{'IsSale': 2}, {'IsSale': None}]
#     }
#     query_2 = {"caption": "$caption", "_id": "$_id"}
#     posts = post_model.collection.find(query_1, query_2)
#     return [doc for doc in posts]
