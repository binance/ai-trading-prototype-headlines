import logging
from datetime import datetime
import importlib
from utils import load_config
from dotenv import load_dotenv
import time


def fetch_headlines(news_source_instance, search_term, start_date, end_date):
    """
    Fetches headlines from a news source based on the provided search term and date range.
    """
    response = news_source_instance.query(search_term, start_date, end_date)
    logging.debug(response.json())
    return news_source_instance.process_data(response)


def write_to_csv(headlines):
    """
    Writes the given headlines to a CSV file.
    """
    written_headlines = []
    with open("./headlines.csv", "w") as f:
        for source, timestamp, headline in headlines:
            if timestamp is not None and headline is not None:
                if headline not in written_headlines:
                    line = '"{}","{}","{}","{}"\n'.format(
                        source, int(time.time() * 1000), timestamp, headline
                    )
                    f.write(line)
                    written_headlines.append(headline)
                    logging.info("Wrote line: " + line)


def main():
    """
    Loads the configuration, sets up logging, and retrieves headlines from various news sources based on the provided search term and date range.
    The headlines are then written to a CSV file.
    """
    load_dotenv()
    cfg = load_config()

    logging_level = cfg["logging_level"]
    logging.basicConfig(level=logging_level, format="%(message)s")

    search_term = cfg["search_term"]
    start_date = datetime.strptime(str(cfg["start_date"]), "%Y-%m-%d")
    end_date = datetime.strptime(str(cfg["end_date"]), "%Y-%m-%d")
    news_sources = cfg["news_sources"]

    headlines = []
    for news_source in news_sources:
        try:
            module = importlib.import_module(f"news_sources.{news_source}")
            news_source_instance = getattr(module, news_source.capitalize())()
            headlines += fetch_headlines(
                news_source_instance, search_term, start_date, end_date
            )
        except (ModuleNotFoundError, AttributeError):
            logging.error(f"News source '{news_source}' not found. Skipping...")
            continue

    write_to_csv(headlines)


if __name__ == "__main__":
    main()
