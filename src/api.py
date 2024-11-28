from io import BytesIO
import joblib
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
# sys.path.append("./../")
from modules.database_modules.mongo_connection import MongoDBConnector
from modules.logger import Logger
from src.update_location import UpdateLocation
# from config.main_config import SAVED_MODEL_PATH, API_ENDPOINT, ping_api_url, doc_url, openapi_filepath
# from config.main_config import logging as logger
# from config.swagger_doc import docs_title, description, version
logger  = Logger().get_logger()
PREFIX_URL = "/dump_to_redis"
ping_api_url = PREFIX_URL + "/ping"
doc_url = PREFIX_URL + "/docs"
API_ENDPOINT = PREFIX_URL + "/get_results"
openapi_filepath = PREFIX_URL + "/openapi.json"

docs_title = "Location Update for HyperLocal News API"

description = """
# Update location coordinates

# For more details, refer to the [documentation](#).

"""

version = "1.0.0"  # Ensure this is a string

# Load the model and pipeline
def load_pipeline(filepath):
	return joblib.load(filepath)


# _saved_objects_1 = load_pipeline(SAVED_MODEL_PATH)
# best_model_pipeline_category, label_encoder_category = _saved_objects_1['pipeline'], _saved_objects_1['label_encoder']
# logger.info(f"loaded model and label encoder from {SAVED_MODEL_PATH}")

# Initialize FastAPI
app = FastAPI(
	title=docs_title
)

# Add CORS middleware to allow requests from any origin (you can tighten this later)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # Allow all origins, modify as needed
	allow_credentials=True,
	allow_methods=["*"],  # Allow all HTTP methods
	allow_headers=["*"],  # Allow all headers
)

@app.get("/", tags=["HEALTH"])
async def read_root():
	"""
	Asynchronous function that handles the root endpoint.
	Returns:
		dict: A dictionary containing a welcome message.
	"""
	return {"message": "Hello World"}

# Health check endpoint
@app.get("/ping", tags=["HEALTH"])
def ping():
	"""
	Health check endpoint to verify if the API is running.
	"""
	return JSONResponse(content={"message": "pong!"}, status_code=200)


# Main endpoint to upload and process files
@app.post("/update", tags=["UPDATE"])
async def upload(file: UploadFile = File(...)):
	"""
	Upload a file and process it to update city coordinates.

	Input:
	- Excel file containing city names and coordinates

	Output:
	- JSON response indicating success or failure
	"""

	try:
		contents = file.file.read()
		with open(file.filename, 'wb') as f:
			f.write(contents)
		xl = pd.ExcelFile(file.filename)
		logger.info(f"Loaded the sheets from attached excel file: {file.filename}")
		# Step 2: Parse the sheets and classify the text
		updater = UpdateLocation()
		for sheet_name in xl.sheet_names:
			_df = xl.parse(sheet_name)  # Read a specific sheet to DataFrame
			# Initialize UpdateLocation instance
			updater.add_new_entries_from_dataframe(_df)
			# Add new entries from the DataFrame
			# for index, row in _df.iterrows():
			# 	updater.add_new_entries_from_dataframe()
			# 	updater._add_new_entry_city(row['city_name'], row['latitude'], row['longitude'])
			return JSONResponse(content={"message": "File processed successfully"}, status_code=200)

	except Exception as e:
		logger.error(f"There was an error uploading the file: {file.filename}, Error: {e}")
		return JSONResponse(content={"message": f"There was an error uploading the file: {file.filename}, Error: {str(e)}"}, status_code=500)
	finally:
		logger.info("Successfully closed temporary files and in-memory objects.")
		file.file.close()
