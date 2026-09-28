import pymongo

myclient = pymongo.MongoClient("mongodb://mongodb:27017/")
mydb = myclient["db"]
mycol = mydb["runs"]



