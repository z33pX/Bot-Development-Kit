import time
import os
import json
import ccxt
import pandas as pd
import logging
logger = logging.getLogger('Fetch Data')

PATH = str(os.path.dirname(os.path.abspath(__file__))) + '/'
CACHE_FOLDER = 'cached_data/'


seconds = {
    '1s': 1,
    '5s': 5,
    '10s': 10,
    '30s': 30,
    '1m': 60,
    '2m': 120,
    '3m': 180,
    '4m': 240,
    '5m': 300,
    '10m': 600,
    '12m': 720,
    '13m': 780,
    '14m': 840,
    '15m': 900,
    '20m': 1200,
    '30m': 1800,
    '40m': 2400,
    '1h': 3600,
    '2h': 7200,
    '3h': 10800,
    '4h': 14400,
    '5h': 18000,
    '6h': 21600,
    '12h': 43200,
    '1d': 86400,
    '2d': 172800,
}


def fetch_ohlc(exchange, pair, interval='5m', convert_to_dataframe=True):
    logger.info('Loading markets of ' + exchange)
    exc = getattr(ccxt, exchange)({'enableRateLimit': True})
    exc.load_markets()

    logger.info('Loading ' + pair + ' data from ' + exchange)
    data = exc.fetch_ohlcv(pair, interval)
    if not convert_to_dataframe:
        return data

    labels = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    return pd.DataFrame.from_records(data, columns=labels)


class FetchData:

    def __init__(self,):
        self.cache_data = dict()
        self.run = True

    def __cache_to_json(self, data, pair, exchange):
        if '/' in pair:
            pair = pair.replace('/', '_')

        file = PATH + CACHE_FOLDER + exchange + '_' + pair + '.json'
        index = str(len(self.cache_data))
        self.cache_data[index] = data

        with open(file, 'w+') as fp:
            json.dump(self.cache_data, fp, indent=4)

    def stop(self):
        self.run = False
        logger.info('Stoped fetching data')

    def fetch_real_time(self, exchange, pair, ohlc_interval='1m', history_length=1, tick_interval=1, n=None):

        if tick_interval > seconds[ohlc_interval]:
            raise ValueError('Tick interval (' + str(tick_interval) +
                             ') cannot be greater than ohlc interval (' +
                             ohlc_interval + '=' + str(seconds[ohlc_interval]) + ')')

        logger.info('Loading markets of ' + exchange)
        exc = getattr(ccxt, exchange)({'enableRateLimit': True})
        exc.load_markets()

        logger.info('Start fetching data: exchange: ' + exchange + ', pair: ' +
                    pair + ', ohlc interval: ' + ohlc_interval +
                    ', history length: ' + str(history_length) +
                    ', tick interval: ' + str(tick_interval))

        tick_interval_count = 1
        ohlc_interval_count = 1

        tick_open = None
        tick_high = list()
        tick_low = list()
        tick_base_volume = list()
        tick_quote_volume = list()

        ohlc_data_hist = list()

        while self.run:
            try:
                data = exc.fetch_ticker(pair)

                if tick_open is None:
                    tick_open = data['open']

                tick_high.append(data['high'])
                tick_low.append(data['low'])
                # TODO Calculate Volume right
                tick_base_volume.append(data['baseVolume'])
                # TODO Calculate Volume right
                tick_quote_volume.append(data['quoteVolume'])

                self.__cache_to_json(data, pair, exchange)

                if (tick_interval_count * tick_interval) % seconds[ohlc_interval] == 0:
                    ohlc_data = [
                        time.time(),
                        tick_open,
                        max(tick_high),
                        min(tick_low),
                        data['close'],
                        tick_base_volume[-1],
                        tick_quote_volume[-1]
                    ]
                    ohlc_data_hist.append(ohlc_data)

                    if len(ohlc_data_hist) >= history_length:
                        yield ohlc_interval_count, ohlc_data_hist[-history_length:]
                        ohlc_interval_count += 1
                    else:
                        yield ohlc_interval_count, 'logging'

                    tick_open = None

                tick_interval_count += 1
                if n is not None:
                    if ohlc_interval_count > n:
                        self.stop()

                if self.run:
                    time.sleep(tick_interval)

            except Exception as e:
                logger.exception(str(e))
