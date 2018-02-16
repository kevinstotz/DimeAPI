from DimeAPI.models import Currency, DimeMutualFund, Xchange, CryptoCompareCoin
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, time
import logging
import time, requests

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


class CryptoCompareUtil():

    def __init__(self, xchange_id=1, comparison_currency='USD'):
        #  instance variable unique to each instance

        self.xchange = Xchange.objects.get(pk=xchange_id)
        self.comparison_currency = comparison_currency
        self.coin_list_url = 'https://www.cryptocompare.com/api/data/coinlist/'

    def updateCoinList(self):

        try:
            coin_list = requests.get(self.coin_list_url).json()
        except ObjectDoesNotExist as error:
            self.currency = 0
            logging.debug('Currency does not exist:{0} {1}:'.format(coin_list.errors, error))

        for coinKey, coinVals in coin_list['Data'].items():

            try:
                cryptoCoin = CryptoCompareCoin.objects.get(xchange_coin=int(coinVals['Id']))
                logging.debug('Updating :{0}'.format(coinVals['Name']))
            except ObjectDoesNotExist as error:
                cryptoCoin = CryptoCompareCoin()
                logging.debug('Adding :{0}'.format(coinVals['Name']))
            try:
                local_currency = Currency.objects.get(symbol=coinVals['Symbol'])
                logging.debug('Updating Local Currency:{0}:'.format(coinVals['Name']))
            except ObjectDoesNotExist as error:
                local_currency = Currency(name=coinVals['Name'],
                                          symbol=coinVals['Symbol'],
                                          coinName=coinVals['CoinName'],
                                          fullName=coinVals['FullName'])
                local_currency.save()
                logging.debug('Adding Local Currency:{0}:'.format(coinVals['Name']))

            cryptoCoin.xchange_coin = coinVals['Id']
            cryptoCoin.url = coinVals['Url']
            if 'ImageUrl' in coinVals:
                cryptoCoin.image_url = coinVals['ImageUrl']
            cryptoCoin.name = coinVals['Name']
            cryptoCoin.symbol = coinVals['Symbol']
            cryptoCoin.coin_name = coinVals['CoinName']
            cryptoCoin.full_name = coinVals['FullName']
            cryptoCoin.algorithm = coinVals['Algorithm']
            cryptoCoin.proof_type = coinVals['ProofType']
            if coinVals['TotalCoinSupply'] == "N/A":
                cryptoCoin.total_coin_supply = 0
            else:
                cryptoCoin.total_coin_supply = coinVals['TotalCoinSupply'].replace(" ", "").replace(".", "").replace(",", "").replace('\u200b', "")
            if coinVals['TotalCoinsFreeFloat'] == "N/A":
                cryptoCoin.total_coins_free_float = 0
            else:
                cryptoCoin.total_coins_free_float = coinVals['TotalCoinsFreeFloat']
            cryptoCoin.sort_order = 0
            cryptoCoin.sponsored = coinVals['Sponsored']

            cryptoCoin.xchange = self.xchange
            cryptoCoin.local_coin = local_currency
            cryptoCoin.save()

    def updateSpotPrice(self, date_of_request='2017-12-23'):
        date_of_request = datetime.strptime(date_of_request, '%Y-%M-%d')
        for dime_index in DimeMutualFund.objects.filter(rebalanceDate=date_of_request):
            currency = Currency.objects.get(pk=dime_index.currency.pk)
            dime_index.rebalance_price = self.getSpotPrice(currency, date_of_request.timetuple())

    def getSpotPrice(self, currency, date_of_request=datetime.utcnow().timetuple()):
        url = '{0}/pricehistorical?fsym={1}&tsyms={2}&ts={3}'.format(self.xchange.api_url,
                                                                     currency.cryptoCompareCoin.symbol,
                                                                     self.comparison_currency,
                                                                     int(time.mktime(date_of_request)))
        spot_price_reponse = requests.get(url)
        spot_price = spot_price_reponse.json()
        return(spot_price[currency.cryptoCompareCoin.symbol][self.comparison_currency])

    def getCoinSnapShot(self, currency_symbol):
        url = '{0}/coinsnapshot?fsym={1}&tsym={2}'.format(self.xchange.api_url,
                                                          currency_symbol,
                                                          self.comparison_currency)
        snap_shot_reponse = requests.get(url)
        return(snap_shot_reponse.json())

    def getCoinMarketCap(self, currency_symbol):
        coin_snap_shot = self.getCoinSnapShot(currency_symbol)
        return(coin_snap_shot.Data.TotalCoinsMined)

    def getCoinPrice(self, currency_symbol):
        coin_snap_shot = self.getCoinSnapShot(currency_symbol)
        return(coin_snap_shot.Data.TotalCoinsMined.AggregatedData.PRICE)