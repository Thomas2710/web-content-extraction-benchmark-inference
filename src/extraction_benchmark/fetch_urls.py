import requests
import json
from extraction_benchmark import fetchers


def fetch_urls(source, domain, keyword, language, mode, timespan):
    """
    Fetch URLs from source
    """
    cls, fetcher_name = (getattr(fetchers, source), source)
    fetcher = cls()
    fetcher.get_data(domain = domain, keyword = keyword, language = language, mode = mode, timespan = timespan)
