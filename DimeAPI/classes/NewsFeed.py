from django.core.exceptions import ObjectDoesNotExist
from DimeAPI.models import Xchange
import json
import requests
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')


class NewsFeed(object):
    # class variable shared by all instances
    rss_server = None
    def __init__(self, rss_server):
        self.rss_server = rss_server
        try:
            self.rss_feed = Xchange.objects.get(pk=rss_server)
        except ObjectDoesNotExist as error:
            logger.error("{0} not found {1}".format(rss_server, error))

    def get_news_feed(self, symbol):
        url = self.rss_feed.api_url + "?auth_token=" + self.rss_feed.api_key + '&currencies=' + symbol
        response = requests.get(url)
        if response.status_code != 200:
            return None
        articles = json.loads(response.content)

        articles_array = []
        for idx, article in enumerate(articles['results']):
            articles_json = {}
            articles_json['title'] = article['title']
            articles_json['date'] = article['published_at']
            articles_json['symbol'] = article['currencies'][0]['code']
            articles_json['domain'] = article['source']['domain']
            articles_array.append(articles_json)
            if idx == 2: return articles_array

