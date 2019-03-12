import sqlite3
import pandas
from sqlite3 import Error

database = './marf.sql'

newDB = './localdata.db'

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

cols = ['cardName', 'setName', 'blue', 'green', 'white', 'black', 'red', 'cardPriceUSD', 'foil', 'foilPrice']


# data = pandas.read_csv('cardData.csv', usecols=cols,sep=';', encoding='utf-8')
# data = data.values.tolist()
con = sqlite3.connect('./localdata.db')
cur = con.cursor()

# colString = ', '.join(cols)

# tableCommand = "CREATE TABLE magicCards (cardName, setName, blue, green, white, black, red, cardPriceUSD, foil, foilPrice);"
# populateTable = "INSERT INTO magicCards (cardName, setName, blue, green, white, black, red, cardPriceUSD, foil, foilPrice) " \
#                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" (data)
#cur.execute(tableCommand)
# cur.executemany("INSERT INTO magicCards (cardName, setName, blue, green, white, black, red, cardPriceUSD, foil, foilPrice) " \
#                 "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (data))

cur.execute('SELECT * FROM magicCards;')
rows = cur.fetchall()

con.commit()
con.close()