import logging
import os

current_path = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(current_path, 'parser.log')
my_logger = logging.getLogger('parser')
my_logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(log_file)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
my_logger.addHandler(file_handler)
my_logger.addHandler(stream_handler)