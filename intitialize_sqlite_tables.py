conn = sqlite3.connect('predictit.db')
cursor = conn.cursor()
# Create tables (only need to do this once)

cursor.execute('''CREATE TABLE questions
             (name text, ID text, ticker text, short_name text, time_stamp text, status text, image_url text, category text, category_url text)''')

cursor.execute('''CREATE TABLE contracts
             (name text, ID text, question text, ticker text, short_name text, long_name text, date_end text, status text, image_url text, last_trade_price real, best_buy_yes real, best_buy_no real, best_sell_yes real, best_sell_no real, last_close_price real)''')

conn.close()
