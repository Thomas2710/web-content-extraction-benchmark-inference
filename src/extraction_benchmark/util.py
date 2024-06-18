# Copyright 2023 Janek Bevendorff
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import re
import requests
from bs4 import BeautifulSoup
import os
import hashlib

def read_jsonl(file):
    """
    Read JSONL file and return iterable of dicts.

    :param file: input filename
    :return: iterable of dicts
    """
    with open(file, 'r') as f:
        for line in f:
            yield json.loads(line)


def jsonl_to_dict(file):
    """
    Load a JSONL into a single dict with ``"page_id"`` as keys.

    :param file: input file name
    :return: assembled dict
    """
    loaded = {}
    for j in read_jsonl(file):
        loaded[j['page_id']] = {k: v for k, v in j.items() if k != 'page_id'}
    return loaded


_TOKEN_RE_WS = re.compile(r'\s+', flags=re.UNICODE | re.MULTILINE)


def tokenize_ws(text):
    """
    Tokenize text by white space.

    :param text: input text
    :return: list of tokens
    """
    text = text.strip()
    if not text:
        return []
    return _TOKEN_RE_WS.split(text)


_TOKEN_RE_WORDS = re.compile(r'\w+', flags=re.UNICODE)


def tokenize_words(text):
    """
    Tokenize text by extracting Unicode word tokens (skips any non-word tokens).

    :param text: input text
    :return: list of tokens
    """
    return _TOKEN_RE_WORDS.findall(text)


def extract_urls_from_file(file):
    """
    From a given file, extract the list of urls contained in the file and return it

    :param file: input file name
    :return: list of urls
    """

    #TODO: add file detection option
    urls = []
    with open(file) as f:
        for line in f:
            urls.append(line.strip())
    return urls


def extract_html_from_urls(urls:list, path:str):
    custom_path = os.path.join(path, 'custom')
    association_path = os.path.join(path, 'url_association')
    for url in urls:

        response = requests.get(url)
        response.raise_for_status()  # This will raise an error if the request was unsuccessful

        #Hash the file content to get file id
        m = hashlib.sha256()
        m.update(response.content)
        file_id = m.hexdigest()
        file = os.path.join(custom_path, file_id + '.html')
        association = os.path.join(association_path, file_id + '.txt')

        soup = BeautifulSoup(response.content, 'html.parser')

        with open(file, 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        with open(association, 'w', encoding='utf-8') as file:
            file.write(url)

