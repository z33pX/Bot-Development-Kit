import pandas as pd
import os
import json
import logging

logger = logging.getLogger('BTC_XRP_5M')
PATH = str(os.path.dirname(os.path.abspath(__file__))) + '/'
DATASET_FILE = 'BTC_XRP_5min.csv'
LABELSET_FILE = 'labels.json'

class BTC_XRP_5M:

    @staticmethod
    def load_btc_xrp_5min(tail=None):
        path = PATH + DATASET_FILE

        data = pd.read_csv(
            path,
            index_col=0
        )

        data = data[22000:]

        data = data.reset_index()

        if tail is not None:
            logger.info('Loaded BTC_XRP_5M dataset (tail=' + str(tail) + ')')
            return data.tail(tail)
        else:
            logger.info('Loaded BTC_XRP_5M dataset')
            return data

    @staticmethod
    def load_btc_xrp_5min_labels():
        data = None
        try:
            with open(PATH + LABELSET_FILE) as f:
                data = json.load(f)
        except Exception as e:
            logger.error('BTC_XRP_5M: ' + str(e))

        logger.info('Loaded BTC_XRP_5M labels')
        return data
