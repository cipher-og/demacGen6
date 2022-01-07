import sqlite3
import alpaca_trade_api
import CONFIG

api = alpaca_trade_api.REST(CONFIG.API_KEY, CONFIG.API_SECKEY, CONFIG.LINK, api_version='v2')

connection = sqlite3.connect('_assets.CU/Alpha.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("SELECT symbol FROM apex")
symbols = cursor.fetchall()
for symbol in symbols:
    assets = api.get_asset(symbol=symbol['symbol'])
    cursor.execute(f"""UPDATE apex SET status = \
    '{assets.status}' where symbol ='{symbol['symbol']}'""")

connection.commit()
