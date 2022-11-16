import json
import os
import sys
import uvicorn
from fastapi import FastAPI, Form
from pydantic import BaseModel
from starlette.responses import FileResponse

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)

from startup import run
# import etl.extract as extract
from utils.logger import Logger
import etl.transform as transform

# log = Logger("preprocessing")

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
