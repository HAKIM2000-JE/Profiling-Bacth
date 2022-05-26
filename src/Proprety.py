from bson import ObjectId

import environement
from geopy import distance
import pandas as pd
from service import Service


class Property:
    def __init__(self, DATA_FRAME_PROPERTY,GUEST_LONGITUDE , GUEST_LATITUDE):
        print("START GETING Close Properties !")
        self.DATA_FRAME_PROPERTY = DATA_FRAME_PROPERTY
        self.RADIUS = environement.RADIUS
        self.GUEST_LONGITUDE = GUEST_LONGITUDE
        self.GUEST_LATITUDE = GUEST_LATITUDE
        self.ServiceData = Service()
        # FOR TEST :
        #self.GUEST_LONGITUDE = 48.88067537287254
        #self.GUEST_LATITUDE = 2.135541034163392

    def get_Poperty(self):

        DATA_FRAME_Property = self.DATA_FRAME_PROPERTY


        #print('GETING CENTER POINT!')
        CENTER_POINT = (self.GUEST_LATITUDE, self.GUEST_LONGITUDE)
        List_DATA = []
        for index, row in DATA_FRAME_Property.iterrows():
            # inilialise a empty data
            DATA = {}

            # get position of PROPERTY
            POSITION_OF_PROPERTY_POI = row['poi']
            if POSITION_OF_PROPERTY_POI and isinstance(POSITION_OF_PROPERTY_POI, type({})):
                PROPERTY_COORDINATES = POSITION_OF_PROPERTY_POI['coordinates']

                # 0 si X et Y c'est 1
                if (PROPERTY_COORDINATES[0] <= 90 and PROPERTY_COORDINATES[0] >= -90) and (PROPERTY_COORDINATES[1] <= 90 and PROPERTY_COORDINATES[1] >= -90):

                    TEST_POINT = (
                        PROPERTY_COORDINATES[0], PROPERTY_COORDINATES[1])
                else:
                    continue
                # Calculate distance betwen
                DISTANCE = distance.geodesic(
                    CENTER_POINT, TEST_POINT).km
                # compare radius and distanse

                if DISTANCE <= self.RADIUS:
                    print("{} point is inside the {} km radius from {} coordinate".format(
                        TEST_POINT, self.RADIUS, CENTER_POINT))
                    # Get the PROPERTY :
                    DATA['_id'] = row['_id']
                    List_DATA.append(DATA)
        print( "Number of close Property :", len(List_DATA))
        return pd.DataFrame(list(List_DATA), columns=['_id'])









