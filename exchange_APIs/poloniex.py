import json
from multiprocessing.dummy import Process as Thread
import logging
import websocket
from poloniex import Poloniex

logger = logging.getLogger('Poloniex Ticker')


class PWSTicker(object):

    def __init__(self, api=None):
        self.api = api
        if not self.api:
            self.api = Poloniex()
        self.tick = {}

        iniTick = self.api.returnTicker()
        self._ids = {market: iniTick[market]['id'] for market in iniTick}
        for market in iniTick:
            self.tick[self._ids[market]] = iniTick[market]

        self._ws = websocket.WebSocketApp("wss://api2.poloniex.com/",
                                          on_open=self.on_open,
                                          on_message=self.on_message,
                                          on_error=self.on_error,
                                          on_close=self.on_close)

    def on_message(self, ws, message):
        message = json.loads(message)
        if 'error' in message:
            return logger.error(message['error'])

        if message[0] == 1002:
            if message[1] == 1:
                return logger.info('Subscribed to ticker')

            if message[1] == 0:
                return logger.info('Unsubscribed to ticker')

            data = message[2]
            data = [float(dat) for dat in data]
            self.tick[data[0]] = {'id': data[0],
                                  'last': data[1],
                                  'lowestAsk': data[2],
                                  'highestBid': data[3],
                                  'percentChange': data[4],
                                  'baseVolume': data[5],
                                  'quoteVolume': data[6],
                                  'isFrozen': data[7],
                                  'high24hr': data[8],
                                  'low24hr': data[9]
                                  }

    def on_error(self, ws, error):
        logger.error(str(error))

    def on_close(self, ws):
        if self._t._running:
            try:
                self.stop()
            except Exception as e:
                logger.error(str(e))

            try:
                self.start()
            except Exception as e:
                logger.error(str(e))
                self.stop()
        else:
            logger.info('Poloniex websocket closed!')

    def on_open(self, ws):
        self._ws.send(json.dumps({'command': 'subscribe', 'channel': 1002}))

    @property
    def status(self):
        """
        Returns True if the websocket is running, False if not
        """
        try:
            return self._t._running
        except:
            return False

    def start(self):
        """ Run the websocket in a thread """
        self._t = Thread(target=self._ws.run_forever)
        self._t.daemon = True
        self._t._running = True
        self._t.start()
        logger.info('Poloniex websocket thread started')

    def stop(self):
        """ Stop/join the websocket thread """
        self._t._running = False
        self._ws.close()
        self._t.join()
        logger.info('Poloniex websocket thread stopped/joined')

    def __call__(self, market=None):
        """ returns ticker from mongodb """
        if market:
            return self.tick[self._ids[market]]
        return self.tick
