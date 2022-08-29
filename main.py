import time

import schedule

from eod import tweet_end_of_day_message
from insight import give_insight
from random_stock import tweet_random_stock

# schedule jobs
schedule.every().hour.at(":00").do(tweet_random_stock)
schedule.every().monday.at("17:30").do(tweet_end_of_day_message)
schedule.every().tuesday.at("17:30").do(tweet_end_of_day_message)
schedule.every().wednesday.at("17:30").do(tweet_end_of_day_message)
schedule.every().thursday.at("17:30").do(tweet_end_of_day_message)
schedule.every().friday.at("17:30").do(tweet_end_of_day_message)
schedule.every(10).seconds.do(give_insight)

while True:
    schedule.run_pending()
    time.sleep(1)
