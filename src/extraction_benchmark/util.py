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
import csv
import shutil

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
    urls = []
    #TODO: add file detection option
    if file[-4:] == '.txt':
        with open(file) as f:
            for line in f:
                urls.append(line.strip())

    elif file[-4:] == '.csv':
        with open(file, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                urls.append(row[0])
    
    elif file[-6:] == '.jsonl':
        with open(file, 'r') as f:
            for line in f:
                data = json.loads(line)
                url = data.get('url')  
                if url:
                    urls.append(url)

    return urls

def get_hash_from_file(file:str):
    #Hash the file content to get file id
    m = hashlib.sha256()
    with open(file, 'rb') as f:
        m.update(f.read())
    file_id = m.hexdigest()
    return file_id

def process_html_files(in_dir:str, out_dir:str):
    for html in os.listdir(in_dir):
        file_id = get_hash_from_file(os.path.join(in_dir, html))
        print('file_id is ',file_id)
        shutil.copy2(os.path.join(in_dir, html), os.path.join(out_dir, file_id+'.html'))

def get_hash_from_url(url:str):
    #Hash the file content to get file id
    m = hashlib.sha256()
    #m.update(response.content)
    m.update(url.encode('utf-8'))
    file_id = m.hexdigest()
    return file_id

def extract_html_from_urls(urls:list, path:str):
    processed_path = os.path.join(path, 'processed')
    association_path = os.path.join(path, 'url_association')
    if not os.path.exists(processed_path):
        os.makedirs(processed_path)
    if not os.path.exists(association_path):
        os.makedirs(association_path)

    rvalue = True
    for url in urls:
        try:
            response = requests.get(url)
            #response.raise_for_status()  # This will raise an error if the request was unsuccessful

            file_id = get_hash_from_url(url)

            file = os.path.join(processed_path, file_id + '.html')

            if os.path.isfile(file):
                print('File already exists')
                continue

            association = os.path.join(association_path, file_id + '.txt')

            soup = BeautifulSoup(response.content, 'html.parser')

            with open(file, 'w', encoding='utf-8') as file:
                file.write(soup.prettify())

            with open(association, 'w', encoding='utf-8') as file:
                file.write(url)
        except:
            print('Failed to extract url:', url)
    return rvalue
