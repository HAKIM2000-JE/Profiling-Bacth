from database import Database
from bson.objectid import ObjectId
import pandas as pd
import environement
Database.initialize()


class Service:
    def __init__(self):
        Database.initialize()

    def convert_cursorWithObjID_to_ListWithoutObjID(self, cursor):
        return map(lambda row: {i: str(row[i]) if isinstance(row[i], ObjectId) else row[i] for i in row}, cursor)

    def convert_to_dataFrame(self, ListWithoutOId):
        return pd.DataFrame(list(ListWithoutOId))

    def get_Tags_DataFrame(self, query):
        Cursor_Tags = Database.find(environement.COLLECTION_TAGS, query)
        return self.convert_to_dataFrame(Cursor_Tags)

    def get_Recommendation_DataFrame(self, query):
         return  self.convert_to_dataFrame(Database.DATABASE[environement.COLLECTION_RECOMMENDATION].find(query, {"poi":1,"_id":1} ))


    def get_OnLineChek_DataFrame(self, query):
        return self.convert_to_dataFrame(Database.find(environement.COLLECTION_ONLINECHECK, query))

    def get_PropretBooking_DataFrame(self , query):
        return self.convert_to_dataFrame(Database.DATABASE[environement.COLLECTION_PROPRETYBOOKING].find(query, \
                                                        {"propertyId":1,"adults":1,"children":1,"_id":1,"babies":1,"doubleBeds":1,"singleBeds":1,"sofaBeds":1,"babyBeds":1,"startDate":1} ))

    def get_Property_DataFrame(self , query ):
        return  self.convert_to_dataFrame(Database.DATABASE[environement.COLLECTION_PROPRETY].find(query, {"poi":1,"_id":1} ))

    def get_Country_DataFrame(self, query):
        return self.convert_to_dataFrame(
            Database.DATABASE[environement.COLLECTION_COUNTRY].find({}))

    def get_Region_DataFrame(self, query):
        return self.convert_to_dataFrame(
            Database.DATABASE[environement.COLLECTION_REGION].find({}))
    def get_guestTag(self, query):
        Cursor_Guest_Tag = Database.find(
            environement.COLLECTION_GUEST_TAG, query)
        list_guest_tag = []
        for row in Cursor_Guest_Tag:
            row['guestId'] = row['_id']['guestId']
            row['tagId'] = row['_id']['tagId']
            list_guest_tag.append(row)
        return self.convert_to_dataFrame(list_guest_tag)

    def get_guestCategory(self, query):
        Cursor_Guest_category = Database.find(
            environement.COLLECTION_GUEST_CATEGORY, query)
        list_guest_category = []
        for row in Cursor_Guest_category:
            row['guestId'] = row['_id']['guestId']
            row['category'] = row['_id']['category']
            list_guest_category.append(row)
        return self.convert_to_dataFrame(list_guest_category)

    def get_guestReviews(self, query):
        Cursor_Guest_Reviews = Database.find(
            environement.COLLECTION_GUEST_REVIEWS, query)
        list_guest_reviews = []
        for row in Cursor_Guest_Reviews:
            row['guestId'] = row['_id']['guestId']
            row['recommendationId'] = row['_id']['recommendationId']
            list_guest_reviews.append(row)
        return self.convert_to_dataFrame(list_guest_reviews)