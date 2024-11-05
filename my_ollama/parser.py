import arxiv
import re
from requests.exceptions import HTTPError
from urllib.parse import urlparse

from my_qdrant.db import update_db

client = arxiv.Client()

def is_url(string):
    regex = re.compile(
        r"^(https?://)?(arxiv\.org)/abs/.*$"
    )
    return re.match(regex, string) is not None

def extract_arxiv_id(url):
    path = urlparse(url).path
    if "/abs/" in path:
        return path.split("/abs/")[1]
    return None

def search_article_by_theme(theme):
    theme = theme.lower()

    search = arxiv.Search(
        query=theme,
        max_results=10,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    try:
        results = list(client.results(search))

        if results and all(result.title for result in results):
            return results
        else:
            print("No valid articles found.")
            
    except HTTPError as e:
        print(f"HTTP Error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def search_article_by_id(arxiv_id):
    search = arxiv.Search(
        id_list=[arxiv_id]
    )

    try:
        results = list(client.results(search))

        if results and all(result.title for result in results):
            return results
        else:
            print("No valid articles found.")
            
    except HTTPError as e:
        print(f"HTTP Error occurred: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def search_article(input_data):
    if is_url(input_data):
        arxiv_id = extract_arxiv_id(input_data)
        return search_article_by_id(arxiv_id)
    return search_article_by_theme(input_data)

def get_text_chunks(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def process_query():
    input_data = input("Enter the theme/url of the article or '0' to skip this step:\n")
    
    if input_data == 0:
        return None

    results = search_article(input_data)

    if len(results) == 1:
        text_chunks = get_text_chunks(results[0].summary)
        update_db(text_chunks)
        print("Article successfully added!")

    elif len(results) > 1:
        for idx, result in enumerate(results):
            print(f"Article {idx + 1}: {result.title}")

        result = results[0]
        while True:
            article = input("Enter needed article: ")
            try:
                result = results[int(article) - 1]
                break
            except:
                print("Invalid input, please enter a number from 1 to 10.")

        text_chunks = get_text_chunks(result.summary)
        update_db(text_chunks)
        print("Article successfully added!")