from utils.logger import Logger
from utils.mongo import Mongo
from datetime import datetime, timedelta, time
import json
from typing import List
import requests
import utils.config as cfg
import pandas as pd
username = 'rtp'
password = "P@ssw0rd"
id = 'my_search_001',
max_count = '10000',
status_buckets = '300',
exec_mode = 'oneshot',
output_mode = 'json',
earliest_time = "-24h",
query = 'search index="test" | search ProfPost'
data = {
    'id': id,
    'count': 20000,
    'status_buckets': status_buckets,
    # 'search': 'search index= "test" | search ValidCategory',
    "search": query,
    'exec_mode': exec_mode,
    'output_mode': output_mode,
}

response = requests.post('https://192.168.103.97:8089/servicesNS/rtp/search/search/jobs', data=data,
                         auth=('rtp', f'{password}'), verify=False)
result = json.loads(response.text)
a = json.loads(result["results"][0]["_raw"])
with open("output.txt", "w", encoding="utf-8") as file:
    # Write the string to the file
    json.dump(a["data"], file, ensure_ascii=False)
