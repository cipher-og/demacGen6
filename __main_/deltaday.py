import _market_order
import pandas
import sqlite3
import _trade_strategy
import push_note
import alpaca_trade_api as tradeapi
import CONFIG

api = tradeapi.REST(CONFIG.API_KEY, CONFIG.API_SECKEY, CONFIG.LINK, api_version='v2')
clock = api.get_clock()

if clock.is_open:

    connection = sqlite3.connect('_assets.CU/Alpha.db')
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute("SELECT id,symbol,status,_1day_interval,market_positions FROM apex")
    rows = cursor.fetchall()

    for row in rows:

        try:
            sym_id = row['id']  # id
            sym = row['symbol']  # symbol
            # row['status']  # status [active/de-listed]
            dataframe = pandas.read_sql_query(f"SELECT close FROM {row['_1day_interval']}", connection)
            market_position = row['market_positions']
            price = dataframe['close']
            last_price = float(dataframe['close'][-1:])

            if row['status'] == 'active':
                "STOCK ACTIVE"
                if _trade_strategy.__breakout_(price):
                    "BREAKING OUT"
                    "BUY"
                    if _market_order.buy_order(symbol=sym, sym_id=sym_id, qty=1000, last_price=last_price):
                        "send push note"
                        push_note.send_msg('BUY', 'BREAK_OUT', 'day', sym, last_price, 'ORDER PLACED')

                    elif _market_order.buy_order(symbol=sym, sym_id=sym_id, qty=1000, last_price=last_price) is False:
                        "send push note"
                        push_note.send_msg('BUY', 'BREAK_OUT', 'day', sym, last_price, 'NO BUYING POWER')

                    '''SELL ORDER IS EXECUTED BY MACD SELL'''

                elif _trade_strategy.__macd_stra_(price) and market_position != 'active':
                    "MACD BUY"
                    "NO PREVIOUS POSITIONS"
                    if _market_order.buy_order(symbol=sym, sym_id=sym_id, last_price=last_price):
                        "send push note"
                        push_note.send_msg('BUY', 'MACD', 'day', sym, last_price, 'ORDER PLACED')

                    elif _trade_strategy.__macd_stra_(price) is False:
                        "send push note"
                        push_note.send_msg('BUY', 'MACD', 'day', sym, last_price, 'NO BUYING POWER')

                elif (_trade_strategy.__macd_stra_(price) is False) and market_position == 'active':
                    "MACD SELL"
                    if _market_order.sell_order(symbol=sym, sym_id=sym_id, last_price=last_price):
                        "send push note"
                        push_note.send_msg('SELL', 'MACD', 'day', sym, last_price, 'ORDER PLACED')

                elif _trade_strategy.__rsi_pullback_(price) and market_position != 'active':
                    "RSI BUY"
                    "NO PREVIOUS POSITIONS"
                    if _market_order.buy_order(symbol=sym, sym_id=sym_id, last_price=last_price):
                        "send push note"
                        push_note.send_msg('BUY', 'RSI', 'day', sym, last_price, 'ORDER PLACED')

                    elif _market_order.buy_order(symbol=sym, sym_id=sym_id, last_price=last_price) is False:
                        "send push note"
                        push_note.send_msg('BUY', 'RSI', 'day', sym, last_price, 'NO BUYING POWER')

                elif _trade_strategy.__rsi_pullback_(price) is False:
                    "RSI SELL"
                    if _market_order.sell_order(symbol=sym, sym_id=sym_id, last_price=last_price):
                        "send push note"
                        push_note.send_msg('SELL', 'RSI', 'day', sym, last_price, 'ORDER PLACED')

            else:
                "NONE"

        except TypeError:
            'pass'
