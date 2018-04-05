import pymongo

class Data2Mongo:
    def __init__(self,db_name,coll_name,ip = "127.0.0.1:27017"):
        self.client = pymongo.MongoClient(ip)
        self.db = self.client[db_name]
        self.db_coll = self.db[coll_name]

    def inserdata(self,datalist):
        inserted = self.db_coll.insert_many(datalist,ordered=True)

if __name__ == '__main__':
    a = Data2Mongo("liufan","jiehun")
    a.inserdata([{"i":i,"date":"2017-10-10"} for i in range(10)])

