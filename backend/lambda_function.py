
from typing import Any, List, TypedDict
import requests
import json
import os

OPENAI_KEY = os.environ['OPENAI_KEY']
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

GOOGLE_KEY = os.environ["GOOGLE_KEY"]
GOOGLE_URL = "https://www.googleapis.com/customsearch/v1"

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
        "num": 5
    }

    for i in range(5):
        print(f"retry {i}")
        ret = requests.get(GOOGLE_URL, params)
        print(ret)

        items = ret.json().get("items", [])
        if len(items) > 0:
            return items
    return []

def get_articles(query: str) -> List[Article]:
    items = _get_items_google(query)
    articles = [{"title": item["title"], "url": item["link"]} for item in items]
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
    articles = get_articles(query)
    print(articles)
    return {
        'statusCode': 200,
        'body': json.dumps(articles)
    }

def get_summary(url: str) -> str:
    return "summary"

def run_summary_lambda(event):
    body = json.loads(event["body"])
    assert "article_url" in body, "missing url"
    url = body["article_url"]
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
    print(lambda_handler(None, None))

