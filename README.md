# Bot Development Kit
The Bot Development Kit is a piece of software helping you to invent trading algorithms

```
      ____        _      _____                _  ___ _   
     |  _ \      | |    |  __ \   Welcome    | |/ (_) |  To The
     | |_) | ___ | |_   | |  | | _____   __  | ' / _| |_ 
     |  _ < / _ \| __|  | |  | |/ _ \ \ / /  |  < | | __|
     | |_) | (_) | |_   | |__| |  __/\ V /   | . \| | |_ 
     |____/ \___/ \__|  |_____/ \___| \_(_)  |_|\_\_|\__|
    
     Great companies are built on great products - Elon Musk
```

Install And Start Example
-

1) `git clone https://github.com/z33pX/Bot-Development-Kit.git`
2) `cd Bot-Development-Kit`
3) `./setup.sh` It will do the following:
    ```
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
4) `source venv/bin/activate` When you see the `(venv) ~/...` in your cli you don't have to do this
5) `python main.py`

Which Exchanges And Markets Are Supportet?
-
It's using the [**ccxt**](https://github.com/ccxt/ccxt) library. To find out which markets and exchanges are supported do the following:

Exchanges:
- Open cli and cd in the Bot-Development-Kit folder
- Activate virtualenv: `source venv/bin/activate`
- Then `python`
- Import ccxt: `import ccxt`
- List all exchanges: `ccxt.exchanges`

Markets:
- Open cli and cd in the Bot-Development-Kit folder
- Activate virtual environment: `source venv/bin/activate`
- Then `python`
- Import ccxt: `import ccxt`
- Load exchange. In this case poloniex: `exchange = ccxt.poloniex()` 
- List all markets: `exchange.load_markets().keys()`

Load And Plot Historical Data
-
Load it:
```
import bot_development_kit as bdk
binance_ETH_BTC_5m = bdk.fetch_ohlc('binance', 'ETH/BTC', interval='5m')
```

For plotting the BDK is using the [**mpl_finance_ext**](https://github.com/z33pX/mpl_finance_ext) library (Please follow the link for a more detailed documentation).
```
import bot_development_kit.mpl_finance_ext as mfe
mfe.plot_candlestick(data=binance_ETH_BTC_5m)
```
Result:
![](https://github.com/z33pX/Bot-Development-Kit/blob/master/pic_01.png)

The OHLC data Loop
-
To **start** it just do:
```
for i, data in fd.fetch_real_time('binance', 'ETH/BTC', ohlc_interval='5s', n=4):

    print(i)
    print(data)
```
It will print the data every 5 seconds. The structure of the data is a list in a list: `[ ..., [timestamp, o, h, l, c, base_colume, quote_volume]]`.
The last element in the wrapping list is the latest datapoint.

Arguments of the `fetch_real_time()` function:
- `exchange`: Exchange like binance
- `pair`: Pair like ETH/BTC
- `ohlc_interval`: Interval of the fetched data. Default is 1m = 1 minute
- `history_length`: The function will return the x last ohlc datapoints. Default is 1
- `tick_interval`: Defines how often ticks are loaded. The interval Default is 1  = 1 second
- `n`: If you pass an argument like 5 the for loop will stop when the index is 5. Default is None. 
In that case you have to call the `stop()` function to stop the loop.

To **stop** the loop you can set the `n` argument or call `fd.stop()`.

Logging
-
If you want to log use
```
bdk.logger.info('I love logging stuff')
```
You can find the logfiles at `bot_development_kit/log_files`