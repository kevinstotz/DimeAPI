from DimeAPI.models import Currency, Period, DimeMutualFund, Vendor
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from coinbase.wallet.client import Client
from coinbase.wallet import auth
from datetime import datetime, time
import logging
import json, hmac, hashlib, time, requests
from requests.auth import AuthBase

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


class GdaxUtil():

    def __init__(self,_vendor_id=1, _currency_id=1, _comparison_currency='USD'):
        #  instance variable unique to each instance
        self.currency = _currency_id
        self.comparison_currency = _comparison_currency
        self.vendor_id = _vendor_id  # coinbase
        self.client = 0

        try:
            self.vendor = Vendor.objects.get(pk=self.vendor_id)
        except ObjectDoesNotExist as error:
            logging.debug('Vendor {0} does not exist:{1}'.format(self.vendor_id, error))
            self.vendor = 0

        try:
            self.client = Client(self.vendor.api_key, self.vendor.api_secret)
        except ObjectDoesNotExist as error:
            logging.debug('Client does not exist:{0}'.format( error))

    def getCurrency(self, currency_id):
        try:
            self.currency = Currency.objects.get(pk=currency_id)
        except ObjectDoesNotExist as error:
            self.currency = 0
            logging.debug('Currency does not exist:{0} {1}:'.format(currency_id, error))
        return self.currency

    def getCurrencyPeriod(self, currency_id, period):
        try:
            self.currency = DimeMutualFund.objects.get(pk=currency_id, period=period)
        except ObjectDoesNotExist as error:
            self.currency = 0
            logging.debug('Currency {0} with period {1} does not exist:{2}'.format(currency_id, period, error))
        return self.currency

    def getSpotPrice(self, date_of_request=datetime.utcnow().isoformat()):
        currency_symbol = self.currency.symbol
        spot_price = self.client.get_spot_price(currency_pair="%s-%s" % (currency_symbol, self.comparison_currency), date=date_of_request )
        return(spot_price)

    def getSpotSupply(self, date_of_request=datetime.utcnow().isoformat()):
        currency_symbol = self.currency.symbol
        spot_price = self.client.get_spot_price(currency_pair="%s-%s" % (currency_symbol, self.comparison_currency), date=date_of_request )
        return(spot_price)