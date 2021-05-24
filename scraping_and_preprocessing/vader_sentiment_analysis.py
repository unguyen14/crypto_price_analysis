from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import ftfy
import pandas as pd
import preprocessor as p # clean tweets

analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    return score


#Apply vader model to our twitter data
df = pd.read_csv('data/consolidatedTweets.csv', dtype="string")

# print(df.shape)

# remove if tweet language is not US, EN or CA
indexNames = df[(df['language'] != 'en')].index
df_en = df.drop(indexNames)

indexNames2 = df[(df['language'] != 'us')].index
df_us = df.drop(indexNames2)

indexNames3 = df[(df['language'] != 'ca')].index
df_ca = df.drop(indexNames3)

df = pd.concat([df_en, df_us, df_ca])

df = df.reset_index()
df = df.drop(["index"], axis=1)

file_name = "tweets_sentiment_v2.csv"

#CLEANING WITH TWEET-PREPROCESSOR

p.set_options(p.OPT.URL, p.OPT.MENTION, p.OPT.HASHTAG)# you can set drop options

df['decoded_tweet'] = df['tweet'].apply(lambda x: ftfy.fix_text(x))

df['tweet'] = df['tweet'].apply(lambda x: p.clean(x))

df = df.dropna(subset=['tweet'])

scores = ['neg', 'neu', 'pos', 'compound']

for score in scores:
    df[score] = df['decoded_tweet'].apply(lambda x: sentiment_analyzer_scores(x)[score])

print(df[{'tweet', 'neg', 'neu', 'pos'}])

df.to_csv("data/tweets_sentiment_v2.csv")
