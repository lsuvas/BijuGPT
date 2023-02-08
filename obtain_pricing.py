import yfinance as yf
import datetime
import MySQLdb as mdb
import shlex

# Obtain a database connection to the MySQL instance
db_host = 'localhost'
db_user = 'sec_user'
db_pass = 'password'
db_name = 'securities_master'
con3 = mdb.connect(db_host, db_user, db_pass, db_name)
con4 = mdb.connect(db_host, db_user, db_pass, db_name)

def obtain_list_of_db_tickers():
  """Obtains a list of the ticker symbols in the database."""
  with con3: 
    cur = con3.cursor()
    cur.execute("SELECT id, ticker FROM symbol where ticker ='AMZN'")
    data = cur.fetchall()
    return [(d[0], d[1]) for d in data]


def get_daily_historic_data_yahoo(ticker):
    #connecting to Yahoo Finance and obtaining the data
    
    ticker_data= yf.Ticker(ticker)  
    yf_data = ticker_data.history(period="1y")    
    yf_data.rename_axis(None,inplace=True)
    yf_data=yf_data.to_string(header=False)
    yf_list=yf_data.split(sep='\n')
     
    prices = []
    for y in yf_list:
        p=shlex.split(y)
        prices.append((p[0],p[2], p[3], p[4], p[5], p[6]))
    return prices

def insert_daily_data_into_db(symbol_id, daily_data):
  """Takes a list of tuples of daily data and adds it to the
  MySQL database. Appends symbol ID to the data.

  daily_data: List of tuples of the OHLC data (with 
  adj_close and volume)"""
  
  # Create the time now
  now = datetime.datetime.utcnow()

  # Amend the data to include the vendor ID and symbol ID
  daily_data = [(symbol_id, d[0], now, now,
    d[1], d[2], d[3], d[4], d[5]) for d in daily_data]

  # Create the insert strings
  column_str = """symbol_id, price_date, created_date, 
          last_updated_date, open_price, high_price, low_price, 
          close_price, volume"""
  insert_str = ("%s, " * 9 )[:-2]
  final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % (column_str, insert_str)

  # Using the MySQL connection, carry out an INSERT INTO for every symbol
  with con4:       
    curs = con4.cursor()
    curs.executemany(final_str, daily_data)
    con4.commit()
 

if __name__ == "__main__":
  # Loop over the tickers and insert the daily historical
  # data into the database
  tickers = obtain_list_of_db_tickers()
  for t in tickers:
    print("Adding data for %s" % t[1])
    yf_data = get_daily_historic_data_yahoo(t[1])
    insert_daily_data_into_db(t[0], yf_data)
   
  
