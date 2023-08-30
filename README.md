# AI Trading Prototype Headlines

This project complements the [ai-trading-prototype](https://github.com/binance/ai-trading-prototype) and [ai-trading-prototype-backtester](https://github.com/binance/ai-trading-prototype-backtester) projects by offering a tool to download news headlines in a compatible format.

 It fetches news headlines and their publication timestamps related to a specific search term from a defined news source, and saves them into a CSV file.

 The headlines can then be used for sentiment analysis, which can be a factor in trading decisions.

## Installation

Clone from GitHub:
```
git clone git@github.com:binance/ai-trading-prototype-headlines.git
```

To run the project, you need to have Python installed and install the required Python packages, which are listed in the `requirements.txt` file. You can install them with pip:

```
cd <path_to_cloned_repository>
pip install -r requirements.txt
```

## Usage

### Configuration

1. Create `config.yaml` from `config.yaml.example` and fill the following settings:
    - `search_term`: The term to search for in the news headlines. For example, if you're interested in trading Bitcoin, you would set this to "bitcoin".
    - `start_date`: The start date for the news search, in the format "YYYY-MM-DD". The search will include articles published on or after this date.
    - `end_date`: The end date for the news search, in the format "YYYY-MM-DD". The search will include articles published on or before this date.
    - `news_sources`: A list of news sources to fetch news headlines. The default is "NewsAPI". Additional options: "Hackernews".
    - `logging_level`: The level of logging. This can be set to "DEBUG", "INFO", "WARNING", "ERROR", or "CRITICAL". The default is "INFO", which logs most messages.

2. Next, you need a free API key from [newsapi.org](https://newsapi.org/register). Once you register for an account, create `.env` from `.env.example` and paste your API key into the `NEWS_API_KEY` variable.

### Running the Project

Run the project with:

```
python src/main.py
```

This will first load all the enabled News Source Classes from `news_sources` directory, as defined in `config.yaml`. It will then use the News Source(s) to fetch news headlines from the specified date-range and save them all into a file named `headlines.csv` in the current directory.

## Example Headlines
Below is an example of the `headlines.csv` file created by this project.
The format is: `"headline collected source","headline collected timestamp (ms)","headline published timestamp (ms)","headline"`
```headlines.csv
"HackerNews","1693197442000","1691417271000","PayPal launches PYUSD stablecoin backed by the US dollar"
"NewsAPI","1693197442000","1690815300000","SEC Reportedly Asked Coinbase to Halt All Trading—Except for Bitcoin"
"NewsAPI","1693197442000","1690898340000","Crypto stocks dip after bitcoin slumps to six-week low - Reuters"
"HackerNews","1693197442000","1691087111000","Razzlekhan and husband guilty of $4.5bn Bitcoin launder"
```

## Contributing

### Adding Custom News Sources
- To add a new news source, create a new Python file in the `news_sources` directory. The new file should consist of a Class with 3 methods: `__init__`, `query` and `process_data`. The Class' name should begin with a capital letter, with the rest of the letters all being lowercase. Eg. `Hackernews`, `Newsapi`.
  - `__init__`: This method should simply initialize the config (`self.config = load_config()`) if neccessary, along with any other variables to be used by the other methods.
  - `query`: This method should return a raw `response` from the news source. In most cases, it will consist of an API call to the relevant News Source API and should return a `response` containing all the articles with their publish dates for the specified date-range.
  - `process_data`: This method should take the raw `response` from the `query` method and return a list of `(timestamp,title)`'s. The `timestamp` should be a unix epoch, eg. `1691381271` and the `title` should be a string containing the news headline.
- Once the Class is created, simply add the filename to the `news_sources` list in the `config.yaml` file in order to enable it.
- Tip: Use the 2 existing news sources as a template/reference.