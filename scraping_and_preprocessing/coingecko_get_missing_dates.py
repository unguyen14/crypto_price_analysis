from pycoingecko import CoinGeckoAPI
import pandas as pd
import datetime
import time

df = pd.DataFrame(columns=['id', 'name', 'price_usd', 'market_cap_usd', 'total_vol_usd','date'])
columns = list(df)
cg = CoinGeckoAPI()

coinIds =["ethereum"]
# coinIds =["bitcoin", "litecoin", "ethereum"]

missingData = pd.read_csv("missedDates.csv")

print(missingData)

consolidatedResults=[]

missedDates=pd.DataFrame(columns=['date','coin'])

consecFailures = 0

for index,row in missingData.iterrows():
    try:
        response = cg.get_coin_history_by_id(id=row.coin, date=row.date,market_data="true")
        values = [response['id'],response['name'],response['market_data']['current_price']['usd'],
                                response['market_data']['market_cap']['usd'],
                                response['market_data']['total_volume']['usd'], row.date]
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
            missedDates = missedDates.append({"date": row.date, 'coin': row.coin}, ignore_index=True)
            print(missedDates)
        else:
            time.sleep(5)
            missedDates = missedDates.append({"date": row.date, 'coin': row.coin}, ignore_index=True)
            print(missedDates)
            print('stopped')
        print("consecutive failures = ", consecFailures)



print(df)
print(missedDates)

# Create file unless exists, otherwise append
# Add header if file is being created, otherwise skip it
with open('coingecko.csv', 'a', newline="") as f:
    df.to_csv(f, header=f.tell()==0)

missedDates.to_csv('missedDates.csv')