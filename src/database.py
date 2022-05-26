
import environement
import pandas as pd
import pymongo


class Database(object):
    URI = environement.URL_DATA_BASE
    #DATABASE_NAME = environement.DATA_BASE_NAME
    DATABASE_NAME = "yaago-prod-clone"
    DATABASE = None

    @staticmethod
    def initialize():
        #client = pymongo.MongoClient(Database.URI)
        client = pymongo.MongoClient("mongodb://root:T8GRF2_uB4%2F%3FqCvq@149.202.107.243:29517/?authSource=admin&readPreference=primary&directConnection=true&ssl=false")
        Database.DATABASE = client[Database.DATABASE_NAME]


    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)