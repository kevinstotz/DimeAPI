from DimeAPI.models import  Xchange
from DimeAPI.settings.base import XCHANGE
import logging
import requests

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


class DimeUtil:

    def __init__(self, exchange):
        self.exchange = exchange
        self.marketCapXchange = Xchange.objects.get(pk=XCHANGE['COIN_MARKET_CAP'])

    def getTopCurrencies(self, count=10):
        url = '{0}/ticker/?limit={1}'.format(self.marketCapXchange.api_url, count)
        top_currencies = requests.get(url)
        return top_currencies.json()
