import linecache
import random

import finnhub
import tweepy

from env import (FINNHUB_API_KEY, TWITTER_ACCESS_TOKEN,
                 TWITTER_ACCESS_TOKEN_SECRET, TWITTER_API_KEY,
                 TWITTER_API_KEY_SECRET)

# constants
NUM_OF_SYMBOLS = 2967 # number of rows in symbols.csv
FILE_NAME = 'symbols.csv'
MAX_CHARS = 280

# setting up api's
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_client = tweepy.API(auth)


def tweet_random_stock():
    while True: # keep getting a new message until less than max allowed characters
        print('Generating tweet...')
        tweet_message = random_stock_template()
        if len(tweet_message) < MAX_CHARS:
            break
    twitter_client.update_status(status=tweet_message)
    print('Tweeted random stock!')

def random_stock_template():     
    profile = ''
    while not profile: # keep trying until finnhub can retrieve the stock (doesn't recognize some symbols)
        print('Attempting to retrieve profile...')
        row = random.randint(0, NUM_OF_SYMBOLS) + 1
        line = linecache.getline(FILE_NAME, row)
        symbol = line.split(',')[0]
        profile = finnhub_client.company_profile2(symbol=symbol)
    
    quote = finnhub_client.quote(symbol=symbol)
    market_cap_num = int(profile['marketCapitalization'])
    if market_cap_num > 1000000:
        market_cap = str(market_cap_num / 1000000) + "T"
    elif market_cap_num > 1000:
        market_cap = str(market_cap_num / 1000) + "B"
    else:
        market_cap = str(market_cap_num) + "M"    
    
    output = f'The Random stock of the hour is {profile["name"]}!\n{profile["name"]} ({symbol}) is a {profile["country"]} based {profile["finnhubIndustry"].lower()} company that trades on the {profile["exchange"]}.\nThe stock currently has a market cap of ${market_cap} and is trading at ${quote["c"]} per share.'
    return output
