import os
import sys
import uvicorn
from fastapi import FastAPI, Form
from starlette.responses import FileResponse
import requests

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)
from etl.transform import run as runt
from startup import run
from etl.load import run as load_run

app = FastAPI()


# class Base(BaseModel):
#     graphql: dict
#
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate_to_json
#
#     @classmethod
#     def validate_to_json(cls, value):
#         if isinstance(value, str):
#             return cls(**json.loads(value))
#         return value


@app.post("/set_mongo")
async def set_mongo(data: dict):
    if data:
        try:
            run(data=data)
            return {'status': "success"}
        except Exception as e:
            return {'status': "failure", 'error': e}
    else:
        # log.warning(f'we have no records')
        return {'status': "empty", 'warning': f'we have no records'}


@app.post("/set_mongo_online")
async def set_mongo_online(data: dict):
    if data:
        try:
            k = 0
            posts = runt(data=data)
            url = "http://192.168.110.45:10004/category_manual_set"
            for post in posts:
                params = {"caption": f"{post['cleaned_caption']}"}
                vec = requests.request("POST", url, params=params)
                if vec.json()['data'][0]['CategoryId'] > 0:
                    k = k + 1
            if k > (len(posts) / 2) - 1:
                load_run(posts)
                return {'status': 1, 'explanation': "yup! it was a cloth shop."}
            else:
                return {'status': 2, 'explanation': "Nope! it was not a cloth shop."}
        except Exception as e:
            return {'status': 3, 'error': e, 'explanation': "the code has not been completed"}
    else:
        # log.warning(f'we have no records')
        return {'status': 4, 'warning': f'we have no records'}


# @app.post("/get_data")
# async def get_data():
#     data = extract.run()
#     if data:
#         parsed_data = transform.run(data)
#         for d in parsed_data:
#             d['_id'] = str(d['_id'])
#         return {'status': 'success', "data": parsed_data}


# @app.post("/preprocessing_manual_set")
# async def manual_set(caption):
#     record = [
#         {'caption': caption}
#     ]
#     parsed_data = transform.run(record)
#     return {'status': 'success', "data": parsed_data}


@app.get("/")
async def read_index():
    return FileResponse('api/index.html')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10020)
