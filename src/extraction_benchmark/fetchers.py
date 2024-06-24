import requests
from abc import ABCMeta, abstractmethod

class Fetcher():
    def __init__(self) -> None:
        pass
    @abstractmethod
    def build_query(self, keyword='', domain='', language=''):
        pass


class gdelt(Fetcher):
    def __init__(self) -> None:
        self.base_url = 'http://api.gdeltproject.org/api/v2/doc/doc?query='
        self.rss_url = 'http://data.gdeltproject.org/gdeltv3/gal/feed.rss'
        pass

    def build_query(self, keyword='', domain='', language=''):
        if not keyword and not domain and not language:
            print('At least one of the following parameters must be provided: keyword, domain, language')
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
    def get_gdelt_data(self, query, mode='ArtList', timespan='1weeks'):
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
        if data and 'articles' in data:
            articles = data['articles']
            for article in articles:
                print(f"Title: {article['title']}")
                print(f"URL: {article['url']}")
                print(f"Date: {article['seendate']}")
                print(f"Source: {article['domain']}\n")
        else:
            print("No articles found")
    
    def get_data(self, keyword='', domain='', language='', mode='ArtList', timespan='1weeks'):
        query = self.build_query(keyword, domain, language)
        data = self.get_gdelt_data(query, mode, timespan)
        print('GDELT returned data type is ', data['articles'])
        return data

# Main function
if __name__ == "__main__":
    # Define your query here
    gdelt_fetcher = GDELT()
    gdelt_fetcher.get_data(keyword='covid', language='english')
