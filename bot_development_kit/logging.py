import coloredlogs
import logging as logging
import os
import datetime
import time

date_today = str(datetime.datetime.fromtimestamp(
    time.time()).strftime('%Y-%m-%d'))

PATH = str(os.path.dirname(os.path.abspath(__file__))) + '/'
if not os.path.exists(PATH + '/log_files'):
    os.makedirs(PATH + '/log_files')

if not os.path.exists(PATH + '/cached_data'):
    os.makedirs(PATH + '/cached_data')

log_file_name =PATH + '/log_files/' + date_today + '.log'
logging.basicConfig(filename=log_file_name, level='INFO')

coloredlogs.install(
    level='INFO',
    datefmt='%Y-%m-%d %I:%M:%S',
    fmt='%(asctime)s %(msecs)03d |%(name)-19s|%(levelname)-8s|%(process)-1d| %(message)s')

logger = logging.getLogger('Bot-Development-Kit')

logger.info(
    """
      ____        _      _____                _  ___ _   
     |  _ \      | |    |  __ \   Welcome    | |/ (_) |  To The
     | |_) | ___ | |_   | |  | | _____   __  | ' / _| |_ 
     |  _ < / _ \| __|  | |  | |/ _ \ \ / /  |  < | | __|
     | |_) | (_) | |_   | |__| |  __/\ V /   | . \| | |_ 
     |____/ \___/ \__|  |_____/ \___| \_(_)  |_|\_\_|\__|
      
    Author: z33p1 - Daniel S.                                                               
    GitHub: https://github.com/z33pX/Bot-Development-Kit
    
    Great companies are built on great products - Elon Musk
    """)