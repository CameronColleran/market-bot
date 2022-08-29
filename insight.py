import finnhub
import tweepy

from env import (FINNHUB_API_KEY, TWITTER_ACCESS_TOKEN,
                 TWITTER_ACCESS_TOKEN_SECRET, TWITTER_API_KEY,
                 TWITTER_API_KEY_SECRET)

FILE_NAME = 'prev_id.txt'
MENTION_KEY_WORD = '#insight'

# connect to api's
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_client = tweepy.API(auth)

def get_last_tweet_id():
    with open(FILE_NAME, 'r') as openfile:
        id = openfile.read()    
    if id == '':
        return ''
    id = int(id.strip())
    return id

def set_last_tweet_id(id):
    f_write = open(FILE_NAME, 'w')
    f_write.write(str(id))
    f_write.close()

def get_mentions():
    most_recent_id = get_last_tweet_id()
    if most_recent_id:
        mentions = twitter_client.mentions_timeline(since_id = most_recent_id)
    else:
        mentions = twitter_client.mentions_timeline()
    return reversed(mentions) # will be empty if no new mentions

def give_insight():
    for mention in get_mentions():
        print(f'Giving insight to tweet #{mention.id}')
        set_last_tweet_id(mention.id)
        if MENTION_KEY_WORD in mention.text.lower():
            symbol = (mention.text.split(MENTION_KEY_WORD, 1)[1]).strip().upper()
            message = stock_profile_template(symbol)
            if message:
                twitter_client.update_status(status = message, in_reply_to_status_id = mention.id, auto_populate_reply_metadata = True)


def stock_profile_template(symbol):
    profile = finnhub_client.company_profile2(symbol=symbol.upper())
    if profile: # if the symbol exists in the finnhub database
        name = profile['name']
        country = profile['country']
        industry = profile['finnhubIndustry'].lower()
        quote = finnhub_client.quote(symbol=symbol.upper())
        output = f'{name} is a {country} based {industry} company.\nIt is currently trading at {quote["c"]}, '
        
        if float(quote["c"]) > float(quote["o"]):
            diff = float(quote["c"]) - float(quote["o"])
            output += f'{diff} more points than what it opened at.'
        elif float(quote["c"]) < float(quote["o"]):
            diff = float(quote["o"]) - float(quote["c"])
            output += f'{round(diff, 2)} less points than what it opened at.'
        else:
            output += 'the same as what it opened at'    

        return output
    else:
        return '' 
