import os
ENV = os.getenv("LOCAL_NEWS_DEPLOY_ENV").strip('\n')
if not ENV:
	ENV = "DEV"

if ENV == 'PROD':
	MONGO_DB_HOST = os.getenv("DS_MONGO_CONN_STR").strip("\n")
	DATABASE = "local-news-staging"

if ENV == 'DEV':
	MONGO_DB_HOST = os.getenv("DS_MONGO_CONN_STR").strip("\n")
	DATABASE = "local-news-dev"
CITY_COLLECTIONS_NAME = "location_cities_v1"
