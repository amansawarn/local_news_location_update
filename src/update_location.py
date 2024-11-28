import os
import sys
sys.path.append("./../")
from modules.database_modules.mongo_connection import MongoDBConnector
from configs.main_config import LAST_UPDATED_TIME, MULTILINGUAL_NAMES_DICT, BLOCK_DICT, \
    STATE_LANGUAGE
from configs.database_config import CITY_COLLECTIONS_NAME
from configsdatabase_config import COLLECTIONS_NAME


class UpdateLocation:
    def __init__(self):
        self.mongo_session = MongoDBConnector().get_connection()
        self.collection = self.mongo_session[CITY_COLLECTIONS_NAME]

    def _add_new_entry_city(self, city_name, latitude, longitude):
        """
        Add new city to the mongo collection
        """
        data = self.collection.find_one({"name_en": city_name})
        if data:
            data["coordinates"] = [latitude, longitude]
            obj_id = data["_id"]
            self.collection.update_one({"_id": obj_id}, {"$set": data})
        else:
            self.collection.insert_one( { "name_en": city_name, "coordinates": [latitude, longitude] })
        return True
    
    def add_new_entries_from_dataframe(self, dataframe):
        """
        Add new city entries to the MongoDB collection from a pandas DataFrame in bulk.
        bool: True if the data was successfully inserted into the collection, False otherwise.
        """
        for index, row in dataframe.iterrows():
            self._add_new_entry_city(row['City'], row['Latitude'], row['Longitude'])
        return True
        # Add new cities to the mongo collection from a pandas dataframe in bulk


if __name__ == "__main__":
    update_location = UpdateLocation()
    print(update_location._add_new_entry_city("Kolkata_dummy", 22.5726, 88.3639))
    # print(update_location._add_new_entries_from_dataframe(dataframe))
# mongo_session = MongoDBConnector().get_connection()

