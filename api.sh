###################################################################################################
#ScriptName         : dump_entities_to_redis
#Version            : 1
#AuthorName         : Aman Sawarn
#Date               : 20/11/2024
#Description        : API to update new location cordinates
###################################################################################################

# Dynamically get the project directory based on the location of this script
project_dir=$(dirname $(realpath $0))
# Today's date
today_date=$(date +%Y/%m/%d)

# Log directory
log_dir="$project_dir/logs/"
mkdir -p $log_dir

# Email recipients for notifications
mail_to_list="aman.sawarn@ril.com"

# Set environment variables
export DEPLOYMENT_ENVIRONMENT="DEV"
status="Success"

# Log file
log_file_name="$log_dir/dump_entities_to_redis.log"

# Run the API with Uvicorn
#uvicorn src.api:app --host 0.0.0.0 --reload --port 8080
