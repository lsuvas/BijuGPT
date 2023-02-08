from bs4 import BeautifulSoup 
import urllib.request
import datetime
import MySQLdb as mdb

from math import ceil

def obtain_parse_wiki_snp500():
  """Download and parse the Wikipedia list of S&P500 
  constituents using requests and libxml.

  Returns a list of tuples for to add to MySQL."""

  # Stores the current time, for the created_at record
  now = datetime.datetime.utcnow()

  # Use libxml to download the list of S&P500 companies and obtain the symbol table
  url='http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
  html=urllib.request.urlopen(url).read()


  page = BeautifulSoup(html,'html.parser')
  symbolslist=[]
  for element in page.table.tbody.contents:
     full_item=[]
     for item in element.stripped_strings:
        full_item.append(item)   
     if full_item !=[]:   
        symbolslist.append(full_item)
  #print(symbolslist)
  
  
  # Obtain the symbol information for each row in the S&P500 constituent table
  symbols = []
  for tds in symbolslist:
       ticker=tds[0]
       name=tds[1]
       sector=tds[3]
       sd = {'ticker': ticker,
       'name': name,
       'sector': sector}
       # Create a tuple (for the DB format) and append to the grand list
       symbols.append( (sd['ticker'], 'stock', sd['name'], 
       sd['sector'], 'USD', now, now) )
  return symbols

def insert_snp500_symbols(symbols):
  """Insert the S&P500 symbols into the MySQL database."""

  # Connect to the MySQL instance
  db_host = 'localhost'
  db_user = 'sec_user'
  db_pass = 'password'
  db_name = 'securities_master'
  con = mdb.connect(host=db_host, user=db_user, passwd=db_pass, db=db_name)

  # Create the insert strings
  column_str = "ticker, instrument, name, sector, currency, created_date, last_updated_date"
  insert_str = ("%s, " * 7)[:-2]
  final_str = "INSERT INTO symbol (%s) VALUES (%s)" % (column_str, insert_str)
  print(final_str, len(symbols))

  # Using the MySQL connection, carry out an INSERT INTO for every symbol
  with con: 
    cur = con.cursor()
    # This line avoids the MySQL MAX_PACKET_SIZE
    # Although of course it could be set larger!
    for i in range(0, len(symbols)):
      cur.execute(final_str, symbols[i])
      con.commit()


if __name__ == "__main__":
  symbols = obtain_parse_wiki_snp500()
  insert_snp500_symbols(symbols)