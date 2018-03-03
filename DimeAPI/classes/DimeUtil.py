
from DimeAPI.serializer import DimePeriodSerializer
from DimeAPI.models import Currency, Period, DimeMutualFund, Xchange
from DimeAPI.settings.base import XCHANGE
from django.core.exceptions import ObjectDoesNotExist
import logging
from datetime import datetime
import requests

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


#  dime_index.calculateDimeIndex(period_id=1)
#  currencyResponse = currency.updateCoinList()
#  currency.updateSpotPrice(date_of_request='2016-12-23')
#  currency.updateSpotPrice(date_of_request='2017-06-23')
#  currency.updateSpotPrice(date_of_request='2017-03-23')
#  currency.updateSpotPrice(date_of_request='2017-09-23')
#  currency.updateSpotPrice(date_of_request='2017-12-23')
#  dime_index.generateDimePeriod(1)
#  dime_index.calculateDimeIndex(period_id=1)
#  dime_index.calculateDimeIndex(period_id=2)
#  dime_index.calculateDimeIndex(period_id=3)
#  dime_index.calculateDimeIndex(period_id=5)


class DimeUtil:

    def __init__(self, exchange):
        self.exchange = exchange
        self.marketCapXchange = Xchange.objects.get(pk=XCHANGE['COIN_MARKET_CAP'])

    def generateDimePeriod(self, period_id):
        try:
            period = Period.objects.get(pk=period_id)
            rebalance_date = str(period.start_year) + '-' + str(period.start_month) + '-' + str(period.start_day)
        except ObjectDoesNotExist as error:
            return('period {0} does not exist {1}'.format(period_id, error))
        idx = 1
        for currency_item in self.getTopCurrencies(count=period.num_of_coins):

            try:
                currency = Currency.objects.get(symbol=currency_item['symbol'])
            except ObjectDoesNotExist:
                print("currency not found locally {0}".format(currency_item['symbol']))
                continue

            try:
                dime_index = DimeMutualFund.objects.get(rebalance_date=rebalance_date, currency=currency)
                print("Dime {0} Exists - updating".format(currency.symbol))
            except ObjectDoesNotExist:
                dime_index = DimeMutualFund()
                dime_index.currency = currency
                print("Dime Index adding {0}".format(currency.symbol))

            dime_index.rebalance_date = rebalance_date
            dime_index.period = period
            dime_index.rank = idx
            idx = idx + 1
            dime_index.price = currency_item['price_usd']
            dime_index.market_cap = float(currency_item['market_cap_usd'])

            dime_index.save()

    def getTopCurrencies(self, count=10):
        url = '{0}/ticker/?limit={1}'.format(self.marketCapXchange.api_url, count)
        top_currencies = requests.get(url)
        return top_currencies.json()

