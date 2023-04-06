
from typing import List, TypedDict
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

def get_articles(query: str) -> List[Article]:
    params = {
        "key": GOOGLE_KEY,
        "cx": "04f1ed0849d3045b0",
        "q": query
    }
    ret = requests.get(GOOGLE_URL, params)
    print(ret)

    items = ret.json().get("items", [])
    articles = [{"title": item["title"], "url": item["link"]} for item in items]
    return articles

def lambda_handler(event, context):
    query = get_search_query("A ‘surreal’ day for Trump in court may only tear the country further apart")
    print(query)
    articles = get_articles(query)
    print(articles)
    return {
        'statusCode': 200,
        'body': json.dumps(articles)
    }

if __name__ == "__main__":
    print(lambda_handler(None, None))
