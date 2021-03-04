import os
import yaml
import pytz
import pandas as pd
from datetime import datetime
import pandas_datareader.data as yahoo_reader
from zipline.utils.calendars import get_calendar
from zipline.api import order_target, symbol, schedule_function, date_rules, time_rules, order_target, order
from zipline.data import bundles
from zipline import run_algorithm
from zipline.gens.brokers.ib_broker import IBBroker
def get_benchmark(symbol=None, start=None, end=None):
    bm = yahoo_reader.DataReader(symbol,
                                 'yahoo',
                                 pd.Timestamp(start),
                                 pd.Timestamp(end))['Close']
    bm.index = bm.index.tz_localize('UTC')
    return bm.pct_change(periods=1).fillna(0)
def initialize(context):
    context.ticker = "AAPL"
    context.sym = symbol(context.ticker)
    print("Initialize.")
def before_trading_start(context, data):
    schedule_function(
            algo_test, 
            date_rules.every_day(), 
            time_rules.market_close(minutes=5))
def handle_data(context, data):
    print("handle data")
def algo_test(context, data):
    context.ticker = "AAPL"
    context.sym = symbol(context.ticker)
    current_price=data.current(context.sym, "price")
    print("current price: ",current_price)
    #buys 10 shares
    order(context.sym, 10)
    print("BUY")
    pass
if __name__ == '__main__':
    bundle_name = 'quantopian-quandl'
    bundle_data = bundles.load(bundle_name)
    print('connecting')
    broker = IBBroker('............')
    print('connected')
    # Set the trading calendar
    trading_calendar = get_calendar('NYSE')
    start = pd.Timestamp(datetime(2020, 1, 1, tzinfo=pytz.UTC))
    end = pd.Timestamp.utcnow()
    account = broker.get_account_from_broker()
    capital_base = float(account['NetLiquidationByCurrency'])
    print(capital_base)
    #exit()
    run_algorithm(start=start,
                  end=end,
                  initialize=initialize,
                  handle_data=handle_data,
                  capital_base=capital_base,
                  benchmark_returns=get_benchmark(symbol="SPY",
                                                  start=start.date().isoformat(),
                                                  end=end.date().isoformat()),
                  bundle='quantopian-quandl',
                  broker=broker,
                  state_filename="./demo.state",
                  trading_calendar=trading_calendar,
                  before_trading_start=before_trading_start,
                  data_frequency='daily'
                  )
