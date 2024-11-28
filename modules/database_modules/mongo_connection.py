
import sys
sys.path.append("./../../..")
from configs.database_config import MONGO_DB_HOST, DATABASE
from pymongo import MongoClient

class MongoDBConnector:

	def get_connection(self):

		db_client = MongoClient(MONGO_DB_HOST)
		db = db_client[DATABASE]
		return db

	def get_mongo_client(self):
		return self.get_connection()