import requests
from bs4 import BeautifulSoup
import datetime
import json
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(
    hosts=[{'host': "localhost", 'port': "9200"}],
    verify_certs=False,
    http_auth=('admin','admin'),
    scheme="https"
)

target_source = "https://m.daum.net/"
portal = "daum"
raw = requests.get(target_source, headers={'User-Agent': 'Mozilla/5.0'})
html = BeautifulSoup(raw.text, "html.parser")

articles = html.select("#channel_news1_top > div:nth-child(1) > div:nth-child(3) > ul > li")

documents = []
for ar in articles:
    title = ar.select_one("a").text
    provider = ar.select_one("a")['data-tiara-provider']
    news_id = ar.select_one("a")['data-tesla-news-id']
    documents.append(
        {
            '_index': "daum-news-articles-v1",
            '_source': {
                "portal": portal,
                "title": title,
                "source": target_source,
                "provider": provider,
                "timestamp": datetime.datetime.now(),
                "newsID": news_id
            }
        }
    )
    helpers.bulk(es, documents)

print(documents)

