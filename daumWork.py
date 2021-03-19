import requests
from bs4 import BeautifulSoup
import datetime
import json
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(hosts="http://news-crawler-es-1426481898.ap-northeast-2.elb.amazonaws.com:9200/")
target_source = "https://m.daum.net/"
portal = "daum"
raw = requests.get(target_source, headers={'User-Agent': 'Mozilla/5.0'})
html = BeautifulSoup(raw.text, "html.parser")

articles = html.select("ul.list_txt.list_rubics.\#news1\#rubics\#txt > li")

documents = []
for ar in articles:
    title = ar.select_one("a").text
    provider = ar.select_one("a")['data-tiara-provider']
    news_id = ar.select_one("a")['data-rubics-news-id']
    documents.append(
        {
            '_index': "daum-news-articles-v1",
            '_source': {
                "portal": portal,
                "title": title,
                "source": target_source,
                "provider": provider,
                "timestamp": str(datetime.datetime.now()),
                "newsID": news_id
            }
        }
    )
    helpers.bulk(es, documents)

print(documents)

