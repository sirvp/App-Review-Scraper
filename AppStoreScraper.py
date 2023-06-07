# APPSTORE REVIEWS SCRAPER
# Scrapes reviews from the last 10 days grom iOS AppStore for the given app in given country, and saves it to a file

import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

# Set the desired parameters
country = "gb"  # Country code for the App Store
app_id = "562202559"  # App ID for ScottishPower
review_count = 200  # Number of reviews to scrape
since_date = datetime.now() - timedelta(days=10)
since_date = since_date.replace(tzinfo=None) 

# Construct the API endpoint URL
url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/sortBy=mostRecent/xml"

# Send a GET request to the API endpoint
response = requests.get(url)

# Parse the HTML response using Beautiful Soup
soup = BeautifulSoup(response.text, "html.parser")

# Find the review entries
entries = soup.find_all("entry")

# Extract the reviews and relevant information
reviews = []
for entry in entries[:review_count]:
    review_date = entry.find("updated").text
    review_date = datetime.strptime(review_date, "%Y-%m-%dT%H:%M:%S%z")  # Parse review date as datetime object
    review_date = review_date.replace(tzinfo=None) 
    if review_date >= since_date:
        review = {
            "version": entry.find("im:version").text,
            "rating": entry.find("im:rating").text,
            "title": entry.find("title").text,
            "content": entry.find("content").text,
            "date": entry.find("updated").text, 
            "username": entry.find("author").find("name").text
        }
        reviews.append(review)

# Specify the path and filename for the CSV file
since_date_str = since_date.strftime("%Y-%m-%d")
csv_file = f"Reviews/ScottishPower_AppStore_Reviews_{since_date_str}.csv"

# Save the reviews into a CSV file
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    fieldnames = ["version","rating","title", "content", "date","username"]  # Updated fieldnames
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(reviews)

print("Reviews saved to", csv_file)