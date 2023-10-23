import os
import sys
import uvicorn
from fastapi import FastAPI
from starlette.responses import FileResponse
import requests
import threading

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)
from etl.transform import run as run_online
from startup import run
from etl.transform import tag_all_post
from mail import Mail
from utils.logger import Logger

app = FastAPI()
log = Logger("ProfPost")


@app.post("/set_mongo")
async def set_mongo(data: dict):
    if data:
        try:
            post_codes = run(data=data)
            return {'status': "success", "codes": post_codes}
        except Exception as e:
            return {'status': "failure", 'error': e}
    else:
        return {'status': "empty", 'warning': f'we have no records'}


@app.post("/set_mongo_online")
async def set_mongo_online(data: dict):
    if data:
        mail = Mail()
        try:
            k = 0
            posts, account = run_online(data=data)
            url = "http://192.168.110.45:10010/account_validator"
            for post in posts:
                params = {"caption": f"{post['cleaned_caption']}",
                          "username": f"{data['username']}",
                          "fullname": f"{data['fullName']}",
                          "categoryname": f"{data['categoryName']}",
                          "bio": f"{data['biography']}",
                          }
                vec = requests.request("GET", url, params=params)
                if vec.json()['data'][0][0] == 1:
                    k = k + 1
            if k / len(posts) > 0.24:
                thread = threading.Thread(
                    target=mail.send, args=(data['latestPosts'][0]['ownerUsername'], data, "it was a cloth shop"))
                thread.start()
                log.info("cloth shop", data=data, valid_post=k, count=len(posts))
                return {'status': 1, 'explanation': "yup! it was a cloth shop."}
            else:
                thread = threading.Thread(
                    target=mail.send(data['latestPosts'][0]['ownerUsername'], data, "it was not a cloth shop"))
                thread.start()
                log.info("not a cloth shop", data=data, valid_post=k, count=len(posts))
                return {'status': 2, 'explanation': "Nope! it was not a cloth shop."}
        except Exception as e:
            thread = threading.Thread(
                target=mail.send(data['latestPosts'][0]['ownerUsername'], data, "interrupted"))
            thread.start()
            log.info("interrupted", data=data)
            return {'status': 3, 'error': e, 'explanation': "the code has not been completed"}
    else:
        log.info("data was empty", data=data)
        return {'status': 4, 'warning': f'we have no records'}


@app.post("/tag_all_post")
async def all_tags_on_post(post: dict):
    if post:
        post_with_tags = tag_all_post(post=post)
        return post_with_tags


@app.post("/tag_all_post_raw_caption")
async def tag_all_post_manual(caption: str):
    post = dict()
    if caption:
        post["caption"] = caption
        post_with_tags = tag_all_post(post=post)
        return post_with_tags


@app.post("/size_manual_set")
async def manual_set(caption: str):
    url = "http://192.168.110.45:10012/size_manual_set"
    params = {"caption": f"{caption}"}
    vec = requests.request("POST", url, params=params)
    return vec.json()


@app.post("/shipping_manual_set")
async def manual_set(caption: str):
    url = "http://192.168.110.45:10011/shipping_manual_set"
    params = {"caption": f"{caption}"}
    vec = requests.request("POST", url, params=params)
    return vec.json()


@app.post("/attribute_manual_set")
async def manual_set(caption: str):
    url = "http://192.168.110.45:10002/attribute_manual_set"
    params = {"caption": f"{caption}"}
    vec = requests.request("POST", url, params=params)
    return vec.json()


@app.post("/price_manual_set")
async def manual_set(caption: str):
    url = "http://192.168.110.45:10009/price_manual_set"
    params = {"caption": f"{caption}"}
    vec = requests.request("POST", url, params=params)
    return vec.json()


@app.post("/brand_manual_set")
async def manual_set(caption: str):
    url = "http://192.168.110.45:10003/brand_manual_set"
    params = {"caption": f"{caption}"}
    vec = requests.request("POST", url, params=params)
    return vec.json()


@app.post("/category_manual_set")
async def manual_set(caption: str):
    url = "http://192.168.110.45:10004/category_manual_set"
    params = {"caption": f"{caption}"}
    vec = requests.request("POST", url, params=params)
    return vec.json()


@app.post("/color_manual_set")
async def manual_set(caption: str):
    url = "http://192.168.110.45:10005/color_manual_set"
    params = {"caption": f"{caption}"}
    vec = requests.request("POST", url, params=params)
    return vec.json()


@app.post("/material_manual_set")
async def manual_set(caption: str):
    url = "http://192.168.110.45:10007/material_manual_set"
    params = {"caption": f"{caption}"}
    vec = requests.request("POST", url, params=params)
    return vec.json()


@app.post("/PostClassifier_manual_set")
async def manual_set(caption: str, username: str, id: str):
    url = "http://192.168.110.45:10035/manual_classifier"
    params = {"caption": caption,
              "username": username,
              "id": id
              }
    vec = requests.request("POST", url, params=params)
    return vec.json()


@app.get("/")
async def read_index():
    return FileResponse('api/index.html')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10020)
