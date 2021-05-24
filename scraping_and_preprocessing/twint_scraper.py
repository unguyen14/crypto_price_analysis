
import twint
import nest_asyncio
import time
import pandas as pd
import random
from datetime import datetime, timedelta

#Calculate date ranges for the search
date1 = '2016-01-01'
date2 = '2021-02-10'
mydates = pd.date_range(date1, date2).tolist()
daterange = []

for item in mydates:
    daterange.append({"since": datetime.strftime(item, '%Y-%m-%d'),
                      "until": datetime.strftime(item + timedelta(days=2), '%Y-%m-%d')})


nest_asyncio.apply()

# Done: "bitcoin", "tezos","cryptocurrency","litecoin", "ethereum"  ,"yearn.finance", "yearn finance", "yfi", "ada", "ltc", "eth",,"xrp", "xtz", "crypto-currency"

cryptocurrencies = ["cryptocurrency"]

# random.shuffle(cryptocurrencies)

for currSearch in cryptocurrencies:
    for each_date in daterange:
        try:
            # Configure
            t = twint.Config()
            t.Search = currSearch
            t.Store_object = True
            t.Limit = 10000000000000000000000000000000000
            t.Lang = "en"
            # t.Filter_retweets = filter_rt.title()
            t.Min_likes = 20
            t.Pandas = True
            # t.Hide_output = True

            t.Until = each_date["until"]
            t.Since = each_date["since"]


            # t.Popular_tweets
            t.Store_csv = True
            t.Output = currSearch + ".csv"

            twint.run.Search(t)

            time.sleep(random.random())

            print(each_date["since"] + " - " + currSearch)

        except:
            print("ERROR: ", currSearch, " - ", each_date)