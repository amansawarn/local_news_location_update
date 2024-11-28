import sys
import logging
import traceback
import datetime
import pytz

sys.path.append("./../")
from configs import logger


class Logger:
	"""
	Logger class based on the python inbuilt logging module with additional functionalities
	"""
	def __init__(self, log_format = logger.LOG_FORMAT, log_level = logger.LOGGING_LEVEL, log_date_format = logger.DATE_FORMAT, timezone = logger.TIMEZONE, log_file = logger.LOGFILE_DUMP_ENTITIES, filemode = logger.FILEMODE):
		"""
		Initialization of Logger class
		
		Keyword Arguments:
			log_format {str} -- log format for the log outputs (default: {config.log_format})
			log_level {str} --  log level (default: {config.log_level})
			log_date_format {str} --  dateformat for the log output (default: {config.date_format})
			timezone {str} --  timezone for the date in log output (default: {config.timezone})
			log_file {str} --  path of logfile creation (default: {config.log_file})
			filemode {str} --  filemode for logfile (default: {config.filemode})
		"""
		# If above are not passed while creating, default will be picked up

		self.timezone = timezone

		self.logger = logging.getLogger("name")
		self.logger.setLevel(log_level)

		std_out_handler = logging.StreamHandler()
		file_out_handler = logging.FileHandler(log_file, mode=filemode)
		formatter = logging.Formatter(fmt=log_format, datefmt=log_date_format)
		formatter.converter = self.local_time
		std_out_handler.setFormatter(formatter)
		self.logger.addHandler(std_out_handler)
		self.logger.addHandler(file_out_handler)
		sys.excepthook = self.log_except_hook
		self.logger.info("Logger is configured")

	def log_except_hook(self, *exc_info):
		"""
		To handle uncaught exceptions
		"""
		text = "".join(traceback.format_exception(*exc_info))
		logging.error("Unhandled exception: %s", text)

	def local_time(self, *args):
		"""
		To convert the time to the passed timezone
		"""
		converted_time = pytz.utc.localize(datetime.datetime.utcnow()).astimezone(pytz.timezone(self.timezone))
		return converted_time.timetuple()

	def get_logger(self):
		"""
		Getter for logger object
		Returns:
			Logger -- logger object with the set configurations
		"""
		return self.logger


if __name__ == '__main__':
	logger = Logger().get_logger()
	logger.info("your message here")
	b = 5/0 # this will automatically be logged to both file and stream, without putting external try-except
	