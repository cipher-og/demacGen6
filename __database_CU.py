import sqlite3

connection = sqlite3.connect('_assets.CU/Alpha.db')
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS apex (
        id INTEGER PRIMARY KEY, 
        symbol TEXT NOT NULL UNIQUE, 
        company TEXT NOT NULL, 
        sector TEXT,
        status TEXT,
        _1hr_interval, 
        _1day_interval,
        market_positions   
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        _date_time
        symbol TEXT NOT NULL UNIQUE,
        market_position,
		quantity,
		price,
		_total_price
	)
""")

connection.row_factory = sqlite3.Row
id_rows = cursor.fetchall()

with open('_assets.CU/decon/company.csv') as intis:
    companies = intis.read().splitlines()
    for company in companies:
        symbol = company.split(',')[0]
        company_name = company.split(',')[1]
        sector = company.split(',')[2]
        try:
            cursor.execute("INSERT INTO apex (symbol, company, sector) \
            VALUES (?, ?, ?)", (symbol, company_name, sector))

        except sqlite3.IntegrityError:
            "pass"

intis.close()

cursor.execute("SELECT id FROM apex")
id_rows = cursor.fetchall()

for row in id_rows:
    _id = row['id']
    cursor.execute(f"""UPDATE apex SET _1hr_interval = \
    '_{_id}_stock_price_1hr' where id = {_id}""")

    cursor.execute(f"""UPDATE apex SET _1day_interval = \
    '_{_id}_stock_price_1day' where id = {_id}""")

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS _{_id}_stock_price_1hr (
                                stock_id INTEGER,
                                date_time NOT NULL,
                                open NOT NULL, 
                                high NOT NULL, 
                                low NOT NULL, 
                                close NOT NULL, 
                                adjusted_close NOT NULL, 
                                volume NOT NULL
                            )
                        """)

    cursor.execute(f"""CREATE TABLE IF NOT EXISTS _{_id}_stock_price_1day (
                                stock_id INTEGER,
                                date_time NOT NULL,
                                open NOT NULL, 
                                high NOT NULL, 
                                low NOT NULL, 
                                close NOT NULL, 
                                adjusted_close NOT NULL, 
                                volume NOT NULL
                            )
                        """)

connection.commit()
