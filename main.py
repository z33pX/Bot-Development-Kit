import bot_development_kit as bdk
import bot_development_kit.mpl_finance_ext as mfe


if __name__ == "__main__":
    fd = bdk.FetchData()

    # Load historical data for backtesting ------------------------------------
    binance_ETH_BTC_5m = bdk.fetch_ohlc('binance', 'ETH/BTC', interval='5m')
    mfe.plot_candlestick(data=binance_ETH_BTC_5m)

    # Run Ticker --------------------------------------------------------------

    try:
        for i, data in fd.fetch_real_time('binance', 'ETH/BTC', ohlc_interval='5s', n=4):

            print(i)
            print(data)

    except KeyboardInterrupt:
        pass

