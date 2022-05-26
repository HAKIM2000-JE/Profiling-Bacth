import pandas as pd
from bson import ObjectId
from flask import jsonify, Flask, request
from tabulate import tabulate
from flask import jsonify
from Proprety import Property
from service import Service
import environement



from Recommendation import  Recommendation

import  Profiling

ServiceData = Service()
def get_Recommendation(propertyBookingId):



    #Reservation Id
    print(propertyBookingId)

    #  propertyId
    propretyId = ServiceData.get_PropretBooking_DataFrame({'_id': ObjectId(propertyBookingId) })['propertyId'][0]

    # poi  property
    guest_property_poi = ServiceData.get_Property_DataFrame({'_id':ObjectId(propretyId)})['poi'][0]
    print("guest property poi : ==>", guest_property_poi['coordinates'][1], guest_property_poi['coordinates'][0])

    #Below intrusction can be done with batch per region
    # get close Property
    PropertyService = Property( ServiceData.get_Property_DataFrame({}) , guest_property_poi['coordinates'][1],
                               guest_property_poi['coordinates'][0])

    # List of resevration for those property
    ListReservation = []



    ListPropertyId=[row['_id'] for index  , row in PropertyService.get_Poperty().iterrows()]

    #Close Reservation list before profiling
    #request from Mongodb with list of propertyId
    #get current and past
    CloseReservation = ServiceData.get_PropretBooking_DataFrame({"propertyId": {"$in": ListPropertyId}})


    #Profiling Service
    ProflingResult = Profiling.getProfiles(CloseReservation).get('objectIdList')
    print(ProflingResult)

    """""""""


    #we got list of  recommendation near of the guest proprety
    RecommendationService = Recommendation(ServiceData.get_Recommendation_DataFrame({}),guest_property_poi['coordinates'][1] ,guest_property_poi['coordinates'][0])
    CloseRecommendation= RecommendationService.get_Recommendation()

    ListRecommendation0=  getProfileRecommendation(ProflingResult[0], CloseRecommendation)
    ListRecommendation1 = getProfileRecommendation(ProflingResult[1], CloseRecommendation)
    ListRecommendation2 = getProfileRecommendation(ProflingResult[2], CloseRecommendation)
    ListRecommendation3 = getProfileRecommendation(ProflingResult[3], CloseRecommendation)
    ListRecommendation4 = getProfileRecommendation(ProflingResult[4], CloseRecommendation)

    """""












#get recommendation List of every Profile
def getProfileRecommendation(ListProfileId, CloseRecommendation):
    List = []

    #on boucle sur les Bonne Adreses
    for index, row in CloseRecommendation.iterrows():
        DATA = {}
        if not ServiceData.get_guestReviews({"_id.recommendationId": row['_id']}).empty:
                        Recommandation_guestReviews = ServiceData.get_guestReviews({"_id.recommendationId": row['_id']})

                        #on recupere l id du voyageur
                        guetId= ObjectId(Recommandation_guestReviews['_id'].tolist()[0]['guestId'])

                        #verification que le voyageur appartinet au profile
                        if (guetId in ListProfileId):
                            DATA['Recommendation Id'] = row['_id']
                            DATA['poi']=row['poi']

                            #calcule du score
                            DATA['SCORE'] = getScore(Recommandation_guestReviews['nbClickRecoCard'],
                                                         Recommandation_guestReviews['nbClickRecoMarker'], \
                                                         Recommandation_guestReviews['nbClickRecoWebSite'],
                                                         Recommandation_guestReviews['nbClickRecoDirection'],
                                                         Recommandation_guestReviews['clickOnSliderPictures'])

                            List.append(DATA)
                        else :
                         print("no score from profile guest ")

    print("outside the boucle :", List)


    RecommendationList=[]
    for element in List:

        RecommendationData = {}


        RecommendationData['Recommendation Id'] = element['Recommendation Id']

        RecommendationData['poi'] = element['poi']
        RecommendationData['score'] = element['SCORE'].tolist()[0]


        RecommendationList.append(RecommendationData)

    #afiichage par score decroissant


    return   RecommendationList











def getScore(nbClickRecoCard,nbClickRecoMarker,nbClickRecoWebSite,nbClickRecoDirection , clickOnSliderPictures):
    NB_score = environement.SCORE_nbClickRecoCard + environement.SCORE_nbClickRecoMarker + environement.SCORE_nbClickRecoWebSite + \
               environement.SCORE_nbClickRecoDirection + \
               environement.SCORE_clickOnSliderPictures

    score = nbClickRecoMarker* environement.SCORE_nbClickRecoMarker + nbClickRecoCard*environement.SCORE_nbClickRecoCard+\
            nbClickRecoDirection* environement.SCORE_nbClickRecoDirection + nbClickRecoWebSite*environement.SCORE_nbClickRecoDirection

    return score /NB_score



def getScoreOnSliderPictures(clickOnSliderPictures):
    print(clickOnSliderPictures)

    if clickOnSliderPictures.bool()==True:
        return environement.SCORE_clickOnSliderPictures
    else:
        return 0











"""""""""
print(RecommendationService.get_Recommendation()['_id'][0])

RecommendationId= RecommendationService.get_Recommendation()['_id'][0]

guestReviewsObject = {ObjectId("624fbed48e9efa4d9fb3cfb7"),ObjectId("61e1cb5ad8020521840ace8b")}



firstRecommendation = ServiceData.get_guestReviews({ "_id.recommendationId": ObjectId("61e1cb5ad8020521840ace8b") } )
print(firstRecommendation.columns)


print("Le score de cette recommendation pour les adults " , getScore(firstRecommendation['nbClickRecoCard'],firstRecommendation['nbClickRecoMarker'], \
      firstRecommendation['nbClickRecoWebSite'] , firstRecommendation['nbClickRecoDirection'] , firstRecommendation['clickOnSliderPictures']))

"""""""""