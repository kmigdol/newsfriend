
import collections
from typing import Any, List, TypedDict
import requests
import json
import os

OPENAI_KEY = os.environ['OPENAI_KEY']
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

GOOGLE_KEY = os.environ["GOOGLE_KEY"]
GOOGLE_URL = "https://www.googleapis.com/customsearch/v1"

BING_KEY = os.environ["BING_KEY"]
BING_URL = "https://api.bing.microsoft.com/v7.0/search"

ARTICLE_COUNT = 5

class Article(TypedDict):
    title: str
    url: str

def make_openai_request(prompt: str) -> dict[str, Any]:
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
    print(ret.json())
    return ret.json()


def get_search_query(headline: str) -> str:
    prompt = f"Give a neutral search query to find more articles given the headline \"{headline}\""
    res = make_openai_request(prompt)
    return res['choices'][0]['message']['content']

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
    print(items)
    articles = [{"title": item["title"], "url": item["link"]} for item in items]
    return articles

def get_articles_bing(query: str) -> List[Article]:
    items = _get_items_bing(query)
    articles = [{"title": item["name"], "url": item["url"]} for item in items]
    return articles

def run_articles_lambda(body):
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

def get_summary(text: str) -> str:
    prompt = f"parse out and write a one paragraph summary from the following article: {text}"
    res = make_openai_request(prompt)

    return res['choices'][0]['message']['content']

def run_summary_lambda(body):
    assert "article_text" in body, "missing text"
    text = body["article_text"]
    print(text)
    summary = get_summary(text)
    print(summary)
    return {
        'statusCode': 200,
        'body': summary
    }

def lambda_handler(event, context):
    print(event)
    try:
        if "body" not in event:
            return {
                'statusCode': 200
            }

        body = json.loads(event["body"])
        if "req_type" in body and body["req_type"] == "summary":    
            return run_summary_lambda(body)
        else:
            return run_articles_lambda(body)
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
    query = "Supreme Court Updates"
    res = get_articles_bing(query)

    print(res)

