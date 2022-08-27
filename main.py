import finnhub
import tweepy
from datetime import date
from env import (FINNHUB_API_KEY, TWITTER_ACCESS_TOKEN,
                 TWITTER_ACCESS_TOKEN_SECRET, TWITTER_API_KEY,
                 TWITTER_API_KEY_SECRET)

# functionality:
# respond to mention for advice on stock
# tweet about a random stock
# beginning of day and/or end of day message/summary

FILE_NAME = 'prev_id.txt'
MENTION_KEY_WORD = '#insight'

# connect to api's
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_client = tweepy.API(auth)

def get_last_tweet_id(file):
    with open(file, 'r') as openfile:
        id = openfile.read()    
    if id == '':
        return ''
    id = int(id.strip())
    return id

def set_last_tweet_id(id, file):
    f_write = open(file, 'w')
    f_write.write(str(id))
    f_write.close()

def get_mentions():
    most_recent_id = get_last_tweet_id(FILE_NAME)
    if most_recent_id:
        mentions = twitter_client.mentions_timeline(since_id = most_recent_id)
    else:
        mentions = twitter_client.mentions_timeline()
    return reversed(mentions)

def give_insight(mention):
    if MENTION_KEY_WORD in mention.text.lower():
        symbol = (mention.text.split(MENTION_KEY_WORD, 1)[1]).upper()


def stock_profile_template(symbol):
    profile = finnhub_client.company_profile2(symbol=symbol.upper())
    name = profile['name']
    country = profile['country']
    industry = profile['finnhubIndustry'].lower()

    return f'{name} is a {country} based {industry} company'