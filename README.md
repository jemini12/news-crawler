# news-crawler + Elasticsearch
Crawling news from daum and naver main.

## Getting Started
Run docker image and that's it!

![daum](daum.png)
![naver](naver.png)

## How it works
This python script uses tools below:
 - Selenium
 - Elasticsearch
 - BeautifulSoup4

By running this script, news title and provider information is gathered. And this script send JSON document to Elasticsearch in AWS.

## More information
- [Elasticsearch](http://news-crawler-es-1426481898.ap-northeast-2.elb.amazonaws.com:9200)
  - index : naver-news-article-v1
  - index : daum-news-article-v1
- [Kibana](http://ec2-54-180-106-15.ap-northeast-2.compute.amazonaws.com:5601)