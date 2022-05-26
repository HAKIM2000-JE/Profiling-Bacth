import time

import pandas as pd
from flask import jsonify, Flask, request

from service import Service
from datetime import date, datetime
import schedule
import batch
from database import Database
from src import environement
import psutil
Database.initialize()


# Importing the library
import psutil

# Calling psutil.cpu_precent() for 4 seconds


import engine
from src.Recommendation import Recommendation

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Service data
ServiceData = Service()






@app.route("/recommendations", methods=['POST'])
def getRecommendation():
    request_data = request.get_json()

    RecommendationFinale=engine.get_Recommendation(request_data['propertyBookingId'])

    print(RecommendationFinale)

    return  str(RecommendationFinale)



if __name__ == "__main__":

    schedule.every().day.at("10:23").do(batch.run)

    while True:
       schedule.run_pending()
       time.sleep(1)

    app.run(debug=False)

    # test in POST MAN :

    # http://127.0.0.1:5000/data

    # http://127.0.0.1:5000/data

