class NewsSource:
    def query(self, search_term, start_date, end_date):
        raise NotImplementedError

    def process_data(self, response):
        raise NotImplementedError

    def validate_response(self, response):
        if response.status_code != 200:
            raise Exception(f"API request failed with status {response.status_code}")
