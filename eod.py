from datetime import date

import finnhub
import tweepy

from env import (FINNHUB_API_KEY, TWITTER_ACCESS_TOKEN,
                 TWITTER_ACCESS_TOKEN_SECRET, TWITTER_API_KEY,
                 TWITTER_API_KEY_SECRET)

# setting up api's
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_client = tweepy.API(auth)

def tweet_end_of_day_message():
    print('Tweeting about IPO\'s...')
    ipo_messages = ipos_template()
    twitter_client.update_status(ipo_messages[0]) # always tweet the first part of the list
    if len(ipo_messages) > 1: # if the list is longer than 1, there was at least 1 ipo, so reply in thread with the ipo's
        first_tweet_id = twitter_client.user_timeline()[0].id # grab id of the tweet we just made so we can reply to it
        for i in range(1, len(ipo_messages)):
            ipo_message = ipo_messages[i]
            twitter_client.update_status(status = ipo_message, in_reply_to_status_id = first_tweet_id, auto_populate_reply_metadata = True)
    
    # TODO:   
    # market news
    # more?

def ipos_template():
    today = str(date.today())

    ipos = finnhub_client.ipo_calendar(_from=today, to=today)['ipoCalendar']
    output = ['Today\'s IPO\'s:\n']
    if ipos:
        for ipo in ipos:
            name = ipo['name']
            symbol = ipo['symbol']
            exchange = ipo['exchange']
            num_shares = str((format(int(ipo['numberOfShares']), ',d')))
            price = ipo['price']
            market_cap = str((format(int(ipo['totalSharesValue']), ',d')))
            output += [f'{name} ({symbol}) IPO\'d today on the {exchange}. The stock opened with {num_shares} shares priced at ${price} per share, and has a current market cap of ${market_cap}.\n']
    else:
        output = ['There were no IPO\'s today!']
    print(len(output))    
    return output

# TODO: implement the rest of this!
def market_news_template():
    market_news = finnhub_client.general_news('general', min_id=0)
    output = ''
    for news in market_news:
        headline = news['headline']
        source = news['source']
        headline = news['headline']
        summary = news['summary']
        url = news['url']
        output += f'Per {source}: \"{headline}\"\nTL;DR: {summary}\nRead more at: {url}\n\n'
    return output.strip()      
