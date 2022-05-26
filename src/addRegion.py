import pandas as pd
from flask import jsonify, Flask, request

from service import Service
from datetime import date, datetime

from database import Database
from src import environement

Database.initialize()

import  Profiling
# Service data
ServiceData = Service()

Country = ServiceData.get_Country_DataFrame({})


for Polygon in Country['features'][0]:
    Region = {}
    Region['name']=Polygon.get('properties').get('nom')
    Region['country']="France"
    geometry={}
    geometry['type']=Polygon.get('geometry').get('type')
    geometry['coordinates']=Polygon.get('geometry').get('coordinates')
    Region['geometry']=geometry

    Database.DATABASE[environement.COLLECTION_REGION].insert_one(Region)


