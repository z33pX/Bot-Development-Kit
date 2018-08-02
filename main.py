import mpl_finance_ext as mfe
from exchange_APIs import Poloniex
from backtest_datasets import BTC_XRP_5M
import bot_development_kit as bdk
import time


if __name__ == "__main__":

    # Load the dataset for backtesting ----------------------------------------
    dataset = BTC_XRP_5M()
    dataset = dataset.load_btc_xrp_5min(tail=500)

    # Plot candlestick chart
    # bdk.logger.info('Plot candlestick chart')
    mfe.plot_candlestick(data=dataset)

    # Run Poloniex Ticker -----------------------------------------------------

    poloniex = Poloniex()
    poloniex.start()

    try:
        pass
        while True:

            print(poloniex('BTC_ETH'))
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    poloniex.stop()