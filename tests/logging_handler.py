import os
import logging

# Set the Variables to False if you don't want to log the details
api_log = True

# Logger for API
api_log_file = 'api_log.txt'
if os.path.exists(api_log_file):
    os.remove(api_log_file)

api_logger = logging.getLogger('api_logger')
api_handler = logging.FileHandler(api_log_file, encoding='utf-8')
api_formatter = logging.Formatter('%(asctime)s - API: %(message)s')
api_handler.setFormatter(api_formatter)
api_logger.addHandler(api_handler)
api_logger.setLevel(logging.INFO)


def log_api(message):
    if api_log:
        api_logger.info(message)


