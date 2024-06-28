import requests
from abc import ABCMeta, abstractmethod
import json
import os
import newsplease
from newsplease import __main__ as newsp


class Fetcher:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def build_query(self, keyword="", domain="", language=""):
        pass

    @abstractmethod
    def save_data(self, data, path):
        pass


class GDELT(Fetcher):
    def __init__(self) -> None:
        self.base_url = "http://api.gdeltproject.org/api/v2/doc/doc?query="
        self.rss_url = "http://data.gdeltproject.org/gdeltv3/gal/feed.rss"
        pass

    def build_query(self, keyword="", domain="", language=""):
        if not keyword and not domain and not language:
            print(
                "At least one of the following parameters must be provided: keyword, domain, language"
            )
            return None

        if domain:
            domain = f"domain:{domain}"
        if language:
            language = f"sourceLang:{language}"
        if keyword:
            keyword = f"{keyword}"
        query = f"{keyword} {domain} {language}"
        return query

    # Function to get GDELT data
    def get_gdelt_data(self, query, mode="ArtList", timespan="1weeks"):
        # Create the request URL
        url = f"{self.base_url}{query}&mode={mode}&timespan={timespan}&format=json"

        # Make the API request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            return data
        else:
            print(f"Error: Unable to fetch data (status code: {response.status_code})")
            return None

    # Function to print articles
    def print_articles(self, data):
        if data and "articles" in data:
            articles = data["articles"]
            for article in articles:
                print(f"Title: {article['title']}")
                print(f"URL: {article['url']}")
                print(f"Date: {article['seendate']}")
                print(f"Source: {article['domain']}\n")
        else:
            print("No articles found")

    def get_data(
        self, keyword="", domain="", language="", mode="ArtList", timespan="1weeks"
    ) -> dict:
        query = self.build_query(keyword, domain, language)
        data = self.get_gdelt_data(query, mode, timespan)
        return data

    # Save data is custom for every class and saves that class data the way it is returned
    def save_data(self, data, file):
        if file[-4:] == ".txt":
            with open(file, "w") as f:
                for article in data["articles"]:
                    f.write(f"{article['url']}\n")


class NPBUILD(Fetcher):
    def __init__(self) -> None:
        pass

    def build_query(self, keyword="", domain="", language=""):
        return domain

    def get_newsbuild_data(self, query) -> object:
        """
        @query: str
        @return: newspaper source object
        """
        from newspaper import build

        urls_set = set()
        articles = []
        fetched_articles = build(query, memoize_articles=False)
        return fetched_articles

    def get_data(self, keyword="", domain="", language="", mode="", timespan=""):
        query = self.build_query(domain=domain)
        data = self.get_newsbuild_data(query)
        return data

    def save_data(self, data, file):
        if file[-4:] == ".txt":
            with open(file, "w") as f:
                for article in data.articles:
                    f.write(f"{article.url}\n")


class NEWSPLEASE(Fetcher):
    def __init__(self) -> None:
        reset_elasticsearch = True
        reset_json = True
        reset_mysql = True
        reset_postgresql = True
        resume = False
        no_confirm = False

        cfg_file_path = os.path.join(os.getcwd(), "crawler_cgf")
        newsp.NewsPleaseLauncher(
            cfg_file_path,
            resume,
            reset_elasticsearch,
            reset_json,
            reset_mysql,
            reset_postgresql,
            no_confirm,
        )

    def build_query(self, keyword="", domain="", language=""):
        pass

    def get_newspls_data(self, query):
        pass

    def get_data(self, keyword="", domain="", language="", mode="", timespan=""):
        query = self.build_query(domain=domain)
        data = self.get_newspls_data(query)
        return data

    def save_data(self, data, file):
        if file[-4:] == ".txt":
            with open(file, "w") as f:
                for article in data.articles:
                    f.write(f"{article.url}\n")


# Main function
if __name__ == "__main__":
    # Define your query here
    fetcher = NEWSPLEASE()
    # gdelt_fetcher = GDELT()
    # gdelt_fetcher.get_data(keyword='covid', language='english')
