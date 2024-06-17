from pymongo import MongoClient
import pandas as pd
from json import loads
from dotenv import load_dotenv
import os

load_dotenv()

data_frame = pd.read_csv(r"C:\Harshal\Data-Science-Projects\shipping-price-prediction\notebooks\data\train.csv")

records = list(loads(data_frame.T.to_json()).values())

client = MongoClient(os.getenv("MONGODB_URL"))

database_name = client["iNeuron"]

collection = database_name["shipping_price"]

collection.insert_many(records)

for i in collection.find():
    print(i)