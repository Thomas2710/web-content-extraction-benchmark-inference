import requests
import json
from extraction_benchmark import fetchers
from extraction_benchmark.paths import *
import os


def fetch_urls(source, domain, keyword, language, mode, timespan):
    """
    Fetch URLs from source
    """
    cls, fetcher_name = (getattr(fetchers, source.upper()), source)
    fetcher = cls()
    data = fetcher.get_data(domain = domain, keyword = keyword, language = language, mode = mode, timespan = timespan)
    filename = 'urls.txt'
    fetcher.save_data(data, os.path.join(CUSTOM_PATH, filename))