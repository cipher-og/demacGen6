import alpaca_trade_api
import sqlite3
import CONFIG
from datetime import date

api = alpaca_trade_api.REST(CONFIG.API_KEY, CONFIG.API_SECKEY, CONFIG.LINK, api_version='v2')
account = api.get_account()

connection = sqlite3.connect('_assets.CU/Alpha.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()


def buy_order(symbol, sym_id, last_price, qty=100):
    total_price = int(last_price) * qty

    if float(account.regt_buying_power) > (total_price + 1000):
        api.submit_order(
            symbol=f'{symbol}',
            qty=qty,
            side='buy',
            type='market',
            time_in_force='day',
        )

        cursor.execute(f"""UPDATE apex SET market_positions = \
            'active' where id = {sym_id}""")
        cursor.execute(f"""UPDATE apex SET quantity = \
                    '{qty}' where id = {sym_id}""")
        cursor.execute(f"""INSERT INTO records (_date_time,symbol,market_position,quantity,price,_total_price) \
            VALUES ('{date.today()}','{symbol}',"buy",'{qty}','{last_price}','{total_price}')""")
        connection.commit()
        return True
    else:
        '''NO BUYING POWER'''
        return False


def sell_order(symbol, sym_id, last_price):
    cursor.execute(f"""SELECT market_positions,quantity FROM apex WHERE id = '{sym_id}'""")
    positions = cursor.fetchall()
    qty = positions['quantity']

    total_price = int(last_price) * qty

    if positions['market_positions'] == 'active':
        api.submit_order(
            symbol=f'{symbol}',
            qty=qty,
            side='sell',
            type='market',
            time_in_force='day',
        )

        cursor.execute(f"""UPDATE apex SET market_positions = \
            'inactive' where id = {sym_id}""")
        cursor.execute(f"""UPDATE apex quantity = \
                    'NULL' where id = {sym_id}""")
        cursor.execute(f"""INSERT INTO records (_date_time,symbol,market_position,quantity,price,_total_price) \
            VALUES ('{date.today()}','{symbol}',"sell",'{qty}','{last_price}','{total_price}')""")
        connection.commit()

        return True

    else:
        '''STOCK not active'''
        return False
