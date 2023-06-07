# PLAYSTORE REVIEWS SCRAPER
# Scrapes reviews from the last 10 days grom Google PlayStore for the given App in given region, and saves it to a file

from google_play_scraper import Sort, reviews
import pandas as pd
from datetime import datetime, timedelta

start_date = datetime.now() - timedelta(days=10)
start_date_str = start_date.strftime("%Y-%m-%d")
result, continuation_token = reviews(
    'uk.co.scottishpower',
    lang='en', # defaults to 'en'
    country='uk', # defaults to 'us'
    sort=Sort.NEWEST, # defaults to Sort.NEWEST
    count=200, # defaults to 100
    filter_score_with=None # defaults to None(means all score)
)

reviews = pd.DataFrame(result)
reviews['at'] = pd.to_datetime(reviews['at'])

new_reviews = reviews[reviews['at']>start_date]
csv_file = f"Reviews/ScottishPower_Playstore_Reviews_{start_date_str}.csv"
new_reviews.to_csv(csv_file, index=False)
print("Reviews saved to ",csv_file)