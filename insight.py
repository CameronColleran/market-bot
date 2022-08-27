import finnhub
from env import FINNHUB_API_KEY

# give some basic insight into the value of a stock

finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

def insight(symbol):
    recommendation_trends = finnhub_client.recommendation_trends(symbol=symbol)
    print(recommendation_trends)

insight('AAPL')