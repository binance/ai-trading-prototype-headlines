from .newssource import NewsSource
import requests
import json


class Hackernews(NewsSource):
    def __init__(self):
        self.source = "HackerNews"

    def query(self, search_term, start_date, end_date):
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        url = f"https://hn.algolia.com/api/v1/search_by_date?query={search_term}&tags=story&numericFilters=created_at_i>={start_timestamp},created_at_i<={end_timestamp}"
        response = requests.get(url)
        return response

    def process_data(self, response):
        data = json.loads(response.text)
        hits = data["hits"]
        headlines = []
        for hit in hits:
            title = hit["title"]
            timestamp = str(hit["created_at_i"] * 1000)
            headlines.append((self.source, timestamp, title))
        return headlines
