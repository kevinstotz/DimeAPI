from django.core.exceptions import ObjectDoesNotExist
from DimeAPI.models import Xchange
import json
from DimeAPI.settings.base import XCHANGE
import requests


class NewsFeed(object):
    # class variable shared by all instances
    rss_server = XCHANGE['CRYPTOPANIC']
    rss_feed = Xchange.objects.get(pk=rss_server)

    def get_news_feed(self, symbol):
        url = self.rss_feed.api_url + "?auth_token=" + self.rss_feed.api_key + '&currencies=' + symbol
        response = requests.get(url)
        articles = json.loads(response.text)

        articles_array = []
        for idx, article in enumerate(articles['results']):
            articles_json = {}
            articles_json['title'] = article['title']
            articles_json['date'] = article['published_at']
            articles_json['symbol'] = article['currencies'][0]['code']
            articles_json['domain'] = article['source']['domain']
            articles_array.append(articles_json)
            if idx == 2: return articles_array


