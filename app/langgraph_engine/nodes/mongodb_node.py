import pymongo
import os

def mongodb_node(state):
    info = state["info"]
    name = info.get("name")

    client = pymongo.MongoClient(os.environ["MONGO_URI"])
    collection = client["chatdb"]["students"]
    result = collection.find_one({"name": name})

    return {"result": result}
