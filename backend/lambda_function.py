
import collections
from typing import Any, List, TypedDict
import requests
import json
import os

OPENAI_KEY =  "" # os.environ['OPENAI_KEY']
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

GOOGLE_KEY = "" # os.environ["GOOGLE_KEY"]
GOOGLE_URL = "https://www.googleapis.com/customsearch/v1"

BING_KEY = "" # os.environ["BING_KEY"]
BING_URL = "https://api.bing.microsoft.com/v7.0/search"


ARTICLE_COUNT = 5

class Article(TypedDict):
    title: str
    url: str

def get_search_query(headline: str) -> str:
    prompt = f"Give a neutral search query to find more articles given the headline \"{headline}\""

    headers = {"Authorization": f"Bearer {OPENAI_KEY}",
               "Content-Type": "application/json"}
    print(headers)
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    print(payload)

    ret = requests.post(OPENAI_URL, json=payload, headers=headers)
    print(ret)
    return ret.json()['choices'][0]['message']['content']

def _get_items_google(query: str):
    params = {
        "key": GOOGLE_KEY,
        "cx": "04f1ed0849d3045b0",
        "q": query,
        "num": ARTICLE_COUNT
    }

    for i in range(5):
        print(f"retry {i}")
        ret = requests.get(GOOGLE_URL, params)
        print(ret)

        items = ret.json().get("items", [])
        if len(items) > 0:
            return items
    return []

def _get_items_bing(query: str):
    headers = {
        "Ocp-Apim-Subscription-Key": BING_KEY
    }
    params = {
        "q": query,
        "count": ARTICLE_COUNT
    }
    res = requests.get(BING_URL, params, headers=headers)
    items = res.json()["webPages"]["value"]
    return items

def get_articles_google(query: str) -> List[Article]:
    items = _get_items_google(query)
    articles = [{"title": item["title"], "url": item["link"]} for item in items]
    return articles

def get_articles_bing(query: str) -> List[Article]:
    items = _get_items_bing(query)
    articles = [{"title": item["name"], "url": item["url"]} for item in items]
    return articles

def run_articles_lambda(event):
    if "body" not in event:
        return {
            'statusCode': 200
        }

    body = json.loads(event["body"])
    assert "title" in body, "missing title"
    article = body["title"]
    query = get_search_query(article)
    print(query)
    articles = get_articles_bing(query)
    print(articles)
    return {
        'statusCode': 200,
        'body': json.dumps(articles)
    }

def get_summary(url: str) -> str:
    params = {
        "SM_API_KEY": SMMRY_KEY,
        "SM_URL": url
    }
    params = collections.OrderedDict(params)
    params.move_to_end("SM_URL")
    res = requests.get(SMMRY_URL, params)

    return res

def run_summary_lambda(event_body):
    assert "article_url" in event_body, "missing url"
    url = event_body["article_url"]
    print(url)
    summary = get_summary(url)
    print(summary)
    return {
        'statusCode': 200,
        'body': summary
    }

def lambda_handler(event, context):
    print(event)
    try:    
        return run_articles_lambda(event)
    except AssertionError as e:
        print(f"VALUE ERROR: {e}" )
        return {
            'statusCode': 400
        }
    except Exception as e:
        print(f"OTHER EXCEPTION {e}")
        return {
            'statusCode': 500
        } 

if __name__ == "__main__":
    event_body = {
        "article_url": 'http://www.bbc.com/news/business-43298897'
    }
    res = get_summary(event_body)
    breakpoint()

    print(res)

