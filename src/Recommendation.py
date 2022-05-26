import environement
from geopy import distance
import pandas as pd


class Recommendation:
    def __init__(self, DATA_FRAME_RECOMMENDATION,GUEST_LONGITUDE , GUEST_LATITUDE):
        print("START GETING RECOMMENDATION  !")
        self.DATA_FRAME_RECOMMENDATION = DATA_FRAME_RECOMMENDATION
        self.RADIUS = environement.RADIUS
        self.GUEST_LONGITUDE = GUEST_LONGITUDE
        self.GUEST_LATITUDE = GUEST_LATITUDE
        # FOR TEST :
        #self.GUEST_LONGITUDE = 48.88067537287254
        #self.GUEST_LATITUDE = 2.135541034163392

    def get_Recommendation(self):
        #print('GET DATAFRAME RECOMMENDATION :' + str(self.GUEST_LATITUDE))
        DATA_FRAME_RECOMMENDATION = self.DATA_FRAME_RECOMMENDATION

        #print('GETING CENTER POINT!')
        CENTER_POINT = (self.GUEST_LATITUDE, self.GUEST_LONGITUDE)
        List_DATA = []
        for index, row in DATA_FRAME_RECOMMENDATION.iterrows():
            # inilialise a empty data
            DATA = {}

            # get position of recommendation
            POSITION_OF_RECOMMENDATION_POI = row['poi']
            if POSITION_OF_RECOMMENDATION_POI and isinstance(POSITION_OF_RECOMMENDATION_POI, type({})):
                RECOMMENDATION_COORDINATES = POSITION_OF_RECOMMENDATION_POI['coordinates']

                # 0 si X et Y c'est 1
                if (RECOMMENDATION_COORDINATES[0] <= 90 and RECOMMENDATION_COORDINATES[0] >= -90) and (RECOMMENDATION_COORDINATES[1] <= 90 and RECOMMENDATION_COORDINATES[1] >= -90):

                    TEST_POINT = (
                        RECOMMENDATION_COORDINATES[0], RECOMMENDATION_COORDINATES[1])
                else:
                    continue
                # Calculate distance betwen
                DISTANCE = distance.geodesic(
                    CENTER_POINT, TEST_POINT).km
                # compare radius and distanse

                if DISTANCE <= self.RADIUS:
                    print("{} point is inside the {} km radius from {} coordinate".format(
                        TEST_POINT, self.RADIUS, CENTER_POINT))
                    # Get the recommendation :
                    DATA['_id'] = row['_id']
                    List_DATA.append(DATA)
        return pd.DataFrame(list(List_DATA), columns=['_id'])
