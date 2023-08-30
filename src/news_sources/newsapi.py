from .newssource import NewsSource
import requests
import os
from utils import convert_iso8601_to_unix_timestamp


class Newsapi(NewsSource):
    def __init__(self):
        self.apikey = os.getenv("NEWS_API_KEY")
        self.source = "NewsAPI"

    def query(self, search_term, start_date, end_date):
        url = f"https://newsapi.org/v2/everything?q={search_term}&from={start_date.isoformat()}&to={end_date.isoformat()}&language=en&sortBy=popularity&apiKey={self.apikey}"
        response = requests.get(url)
        return response

    def process_data(self, response):
        articles = response.json()["articles"]
        headlines = []
        for article in articles:
            title = article["title"]
            timestamp = int(convert_iso8601_to_unix_timestamp(article["publishedAt"]))
            headlines.append((self.source, timestamp * 1000, title))
        return headlines
