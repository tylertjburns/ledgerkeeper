import pandas as pd
import json


def list_mongo_to_pandas(items):
    if len(items) == 0:
        return pd.DataFrame()

    jsonstr = "{ \"data\": ["
    for item in items:
        jsonstr += item.to_json() + ", "
    jsonstr = jsonstr[:-2] + "]}"
    jsonstr = json.loads(jsonstr)
    data = pd.io.json.json_normalize(jsonstr, record_path='data')
    return data