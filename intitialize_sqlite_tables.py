import sqlite3

conn = sqlite3.connect('predictit.db')
cursor = conn.cursor()
# Create tables (only need to do this once)
try:
    cursor.execute('''DROP TABLE questions;''')
except:
    pass
try:
    cursor.execute('''DROP TABLE contracts;''')
except:
    pass
try:
    cursor.execute('''DROP TABLE question_vars;''')
except:
    pass
try:
    cursor.execute('''DROP TABLE contract_vars;''')
except: pass

cursor.execute('''CREATE TABLE questions
             (name text, IRL text, ID text, ticker text, short_name text, time_stamp text, status text, image_url text, category text, category_url text)''')

cursor.execute('''CREATE TABLE contracts
             (name text, IRL text, ID text, question text, ticker text, short_name text, long_name text, image_url text, time_stamp text)''')

cursor.execute('''CREATE TABLE question_vars
               (ID text, time_stamp text, status text)''')
               
cursor.execute('''CREATE TABLE contract_vars
               (ID text, time_stamp text, date_end text, status text, last_trade_price real, best_buy_yes real, best_buy_no real, best_sell_yes real, best_sell_no real, last_close_price real)''')

conn.close()
