import requests
from datetime import datetime, timedelta
import pandas as pd
import time
import random

def scraper(type,start,end):
  if type=='Ethereum':
    url = f"https://api.blockchair.com/ethereum/transactions?q=time({start}..{end})&limit=100"
    response = requests.get(url)
  elif type=='Bitcoin':
    url = "https://api.blockchair.com/bitcoin/transactions"
    limit = 100
    offset = 0
    page = 0
    params1 = {
        "s": "output_total(desc)",
        "q": f"time({start}..{end})",
        "limit": limit,
        "offset": offset,
        "page": page
    }
    response = requests.get(url, params=params1)
  else:
     print("Invalid Type")
  if response.status_code == 200:
      data = response.json()['data']
  else:
      print("Error: ", response.status_code)
  # a dataframe with 100 rows of transactions will get created
  df = pd.DataFrame(data)
  return df

def main():
  start = datetime.now()-timedelta(days=5)
  end = datetime.now()+timedelta(hours=7)
  start = start.strftime("%Y-%m-%d %H:%M:%S")
  end_str = end.strftime("%Y-%m-%d %H:%M:%S")
  #  print(start,end_str)
  #  i = 0
  df = scraper('Ethereum',start,end_str)
  return df
  #  while(True):
      # print(start,end_str)
      # start = end_str
      # end = end + timedelta(hours=7)
      # end_str = end.strftime("%Y-%m-%d %H:%M:%S")
      # n = random.randint(1,10000)
      # df.to_csv(f"{n}.csv",index=False)
      # time.sleep(60)
# main()