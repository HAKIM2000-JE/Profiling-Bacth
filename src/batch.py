from flask import jsonify, Flask, request

from service import Service
from datetime import date, datetime

from database import Database
from src import environement
import psutil
Database.initialize()

import  Profiling

# Importing the library
import psutil

# Calling psutil.cpu_precent() for 4 seconds


import engine
from src.Recommendation import Recommendation

def run():

    ServiceData = Service()

    Regions = ServiceData.get_Region_DataFrame({})
    # on boucle sur les polygones du pays
    for index, Region in Regions.iterrows():
        if Region['geometry'].get('type') == "Polygon":

            Properties = ServiceData.get_Property_DataFrame({"poi": {"$geoWithin": {
                "$geometry": {"type": "Polygon", "coordinates": Region.get('geometry').get('coordinates')}}}})

        else:
            Properties = ServiceData.get_Property_DataFrame({"poi": {"$geoWithin": {
                "$geometry": {"type": "MultiPolygon", "coordinates": Region.get('geometry').get('coordinates')}}}})


        if not Properties.empty:
            DATA = {}

            ListPropertyId = [row['_id'] for index, row in Properties.iterrows()]
            DATA['name'] = Region['name']
            DATA['country'] = Region['country']
            DATA['propertiesIds'] = ListPropertyId
            DATA['geometry']=Region['geometry']
            Database.DATABASE[environement.COLLECTION_REGION].delete_many({"_id": Region['_id']})
            Database.DATABASE[environement.COLLECTION_REGION].insert_one(DATA)

            # Liste des réservation pris dans ces proprietés en passé
            Reservations = ServiceData.get_PropretBooking_DataFrame(
                {"propertyId": {"$in": ListPropertyId}, "startDate": {"$lt": datetime.now().strftime("%Y-%m-%d")}})

            ListInsert = []
            if not Reservations.empty:

                # Service de création des profile
                Profiles = Profiling.getProfiles(Reservations)

                for Profile in Profiles:
                    Profile_Object = {}
                    Profile_Object['regionId'] = Region['_id']
                    Profile_Object['propertyBookingsIds'] = Profile.get('objectIdList')  # Profile.get('propertyBookings')
                    Profile_Object['centroids'] = Profile.get('centroids').tolist()

                    # we got list of  recommendation in the polygon
                    if Region['geometry'].get('type') == "Polygon":

                        Recommendations = ServiceData.get_Recommendation_DataFrame({"poi": {"$geoWithin": {
                            "$geometry": {"type": "Polygon",
                                          "coordinates": Region.get('geometry').get('coordinates')}}}})

                    else:
                        Recommendations = ServiceData.get_Recommendation_DataFrame({"poi": {"$geoWithin": {
                            "$geometry": {"type": "MultiPolygon",
                                          "coordinates": Region.get('geometry').get('coordinates')}}}})

                    if not Recommendations.empty:

                        Recommendation_Output = engine.getProfileRecommendation(Profile.get('objectIdList'),
                                                                                Recommendations)
                        if len(Recommendation_Output) > 0:
                            listRecommendations = []
                            for recommendation in Recommendation_Output:
                                # object RecommendationScore(idRecommendation , score , RecommendationPoi)
                                print("Scored Recommendation", recommendation)
                                RecommendationScore = {}
                                RecommendationScore['recommendationId'] = recommendation.get('Recommendation Id')
                                RecommendationScore['poi'] = recommendation.get('poi')
                                RecommendationScore['score'] = recommendation.get('score')
                                listRecommendations.append(RecommendationScore)

                            Profile_Object['recommendationScores'] = listRecommendations

                            # add function to drop_all  old profiles per region
                            # Insert all insted of insert_one
                            ListInsert.append(Profile_Object)

            if len(ListInsert) > 0:
                Database.DATABASE[environement.COLLECTION_PROFILE].delete_many({"regionId": Region['_id']})
                Database.DATABASE[environement.COLLECTION_PROFILE].insert_many(ListInsert)

        print('The CPU usage is: ', psutil.cpu_percent(5))