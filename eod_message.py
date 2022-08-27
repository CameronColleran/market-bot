from datetime import date
import finnhub
from env import FINNHUB_API_KEY

# series of tweets sent at end of day about today's market news

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

def end_of_day_message():
    # ipo's
    # market news (difficult to fit for character limit)
    # more?
    return

def ipos_template():
    today = str(date.today())

    ipos = finnhub_client.ipo_calendar(_from=today, to=today)['ipoCalendar']
    output = 'Today\'s IPO\'s:\n'
    if ipos:
        for ipo in ipos:
            name = ipo['name']
            symbol = ipo['symbol']
            exchange = ipo['exchange']
            num_shares = str((format(int(ipo['numberOfShares']), ',d')))
            price = ipo['price']
            market_cap = str((format(int(ipo['totalSharesValue']), ',d')))
            output += f'{name} ({symbol}) IPO\'d today on the {exchange}. The stock opened with {num_shares} shares priced at ${price} per share, and has a current market cap of ${market_cap}.\n'
    else:
        output = 'There were no IPO\'s today!'
    return output.strip()

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


print(market_news_template())
