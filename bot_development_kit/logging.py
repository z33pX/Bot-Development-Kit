import coloredlogs
import logging as logging
import os
import datetime
import time

PATH = str(os.path.dirname(os.path.abspath(__file__))) + '/'
date_today = str(datetime.datetime.fromtimestamp(
    time.time()).strftime('%Y-%m-%d'))

logging.basicConfig(
    filename=PATH + '/log_files/' + date_today + '.log',
    level='INFO')

coloredlogs.install(
    level='INFO',
    datefmt='%Y-%m-%d %I:%M:%S',
    fmt='%(asctime)s %(msecs)03d |%(name)-15s|%(levelname)-8s|%(process)-1d| %(message)s')

logger = logging.getLogger('Bot-Development-Kit')

logger.info(
    """
              _ _                 _
        /\   | | |  Welcome  To  | |  The
       /  \  | | |_ _ __ __ _  __| | ___
      / /\ \ | | __| '__/ _` |/ _` |/ _ \ 
     / ____ \| | |_| | | (_| | (_| |  __/
    /_/    \_\_|\__|_|  \__,_|\__,_|\___| v 1.0
    Bot Development Kit - Daniel Schönbohm
    
    Great companies are built on great products - Elon Musk
    """)