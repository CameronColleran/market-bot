import time

import schedule

from eod import tweet_end_of_day_message
from insight import give_insight
from random_stock import tweet_random_stock

HOURLY = ":00"
DAILY = "17:30"
SECOND_INTERVAL = 10

# schedule jobs
schedule.every().hour.at(HOURLY).do(tweet_random_stock)
schedule.every().monday.at(DAILY).do(tweet_end_of_day_message)
schedule.every().tuesday.at(DAILY).do(tweet_end_of_day_message)
schedule.every().wednesday.at(DAILY).do(tweet_end_of_day_message)
schedule.every().thursday.at(DAILY).do(tweet_end_of_day_message)
schedule.every().friday.at(DAILY).do(tweet_end_of_day_message)
schedule.every(SECOND_INTERVAL).seconds.do(give_insight)

while True:
    schedule.run_pending()
    time.sleep(1)
