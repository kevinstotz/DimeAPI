from django.db.models import Sum
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

    def calculateDimeIndex(self, period_id=1):
        period = Period.objects.get(pk=period_id)

        period_start_date = str(period.start_year) + "-" + str(period.start_month) + "-" + str(period.start_day)
        period_start_date = datetime.strptime(period_start_date, '%Y-%M-%D')

        period_end_date = str(period.end_year) + "-" + str(period.end_month) + "-" + str(period.end_day)
        period_end_date = datetime.strptime(period_end_date, '%Y-%M-%D')

        if period_end_date.timestamp() > datetime.utcnow().timestamp():
            period_end_date = datetime.utcnow()

        prior_period = Period.objects.get(pk=(period_id-1))

        prior_period_start_date = str(prior_period.start_year) + "-" + str(prior_period.start_month) + "-" + str(prior_period.start_day)
        prior_period_start_date = datetime.strptime(prior_period_start_date, '%Y-%M-%D')

        total_cap_market_sum = DimeMutualFund.objects.filter(rebalance_date=period_start_date).aggregate(value=Sum('market_cap'))
        index_value = DimeMutualFund.objects.filter(rebalance_date=prior_period_start_date).aggregate(value=Sum('end_value'))
        dime_indexes = DimeMutualFund.objects.filter(rebalance_date=period_start_date).order_by('-market_cap')
        idx = 1

        for dime_index in dime_indexes:
            if period.pk == 1:
                dime_index.level = 10
            else:
                dime_index.level = index_value['value']

            dime_index.percent_of_dime = dime_index.market_cap / total_cap_market_sum['value'] * 100.0
            dime_index.amount = (dime_index.percent_of_dime / 100.0 * dime_index.level) / dime_index.rebalance_price
            dime_index.rebalance_value = dime_index.rebalancePrice * dime_index.amount
            dime_index.rebalance_price = self.exchange.getSpotPrice(dime_index.currency, date_of_request=period_start_date.timetuple())

            dime_index.end_price = self.exchange.getSpotPrice(dime_index.currency, date_of_request=period_end_date.timetuple())
            dime_index.end_value = dime_index.end_price * dime_index.amount
            dime_index.rank = idx
            idx = idx + 1

            dime_index.save()
