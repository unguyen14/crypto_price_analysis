from pycoingecko import CoinGeckoAPI
import pandas as pd
import datetime
import time

df = pd.DataFrame(columns=['id', 'name', 'price_usd', 'market_cap_usd', 'total_vol_usd','date'])
columns = list(df)
cg = CoinGeckoAPI()

#
coinId = "yearn-finance"
# done =["bitcoin", "litecoin", "ethereum", "cardano", "ripple", "tezos"]

# numdays = 4420 # 01-01-2009
numdays = 2970 #01-01-2013

base = datetime.datetime.today()
date_list = [base - datetime.timedelta(days=x) for x in range(numdays)]
formattedDates =[]

for date in date_list:
    formattedDates.append(date.strftime("%d-%m-%Y"))

print(formattedDates)

consolidatedResults=[]

missedDates=pd.DataFrame(columns=['date','coin'])

consecFailures = 0

for date in formattedDates:
    try:
        response = cg.get_coin_history_by_id(id=coinId, date=date,market_data="true")
        values = [response['id'],response['name'],response['market_data']['current_price']['usd'],
                                response['market_data']['market_cap']['usd'],
                                response['market_data']['total_volume']['usd'], date]
        zipped = zip(columns, values)
        dictionary = dict(zipped)
        print(dictionary)
        df = df.append(dictionary, ignore_index=True)
        consecFailures = 0
        # time.sleep(0.1)
    except:
        consecFailures = consecFailures + 1
        if consecFailures > 20:
        # if formattedDates.index(date) > 3330:
            missedDates = missedDates.append({"date": date, 'coin': coinId}, ignore_index=True)
            print(missedDates)
        else:
            time.sleep(5)
            missedDates = missedDates.append({"date": date, 'coin': coinId}, ignore_index=True)
            print(missedDates)
            print('stopped')
        print("consecutive failures = ", consecFailures)



print(df)
print(missedDates)

with open('coingecko.csv', 'a', newline="") as f:
    df.to_csv(f, header=f.tell()==0)

with open('missedDates.csv', 'a', newline="") as f:
    missedDates.to_csv(f, header=f.tell()==0)

# df.to_csv('coingecko.csv')
# missedDates.to_csv('missedDates.csv')