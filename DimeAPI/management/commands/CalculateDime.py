from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from DimeAPI.models import Xchange, DimeFund, DimePeriod, Currency
from django.core.management.base import BaseCommand
from DimeAPI.settings.base import XCHANGE
from datetime import datetime, timedelta
import calendar
from django.apps import apps
from django.db.models import Sum


class Command(BaseCommand):

    def handle(self, *args, **options):

        periods = DimePeriod.objects.all().order_by('start_date')[15:]

        xchange = Xchange.objects.get(pk=XCHANGE['COIN_MARKET_CAP'])

        for period in periods:
            if not self.verify(period, xchange):
                return

        for period in periods:
            self.calculateDime(period, xchange)


    def calculateDime(self, period, xchange):

        period_start_date = period.start_date
        period_end_date = period.end_date

        prior_DimeFund_Value = DimeFund.objects.filter(period__pk=(period.pk-1)).aggregate(Sum('end_value'))
        if period.pk == 2:
            level = 10
        else:
            level = prior_DimeFund_Value['end_value__sum']

        if period_start_date > datetime.utcnow().date():
            return

        if period_end_date > datetime.utcnow().date():
            period_end_date = datetime.utcnow().date() - timedelta(days=1)

        market_cap = dict()
        rebalance_price = dict()
        market_cap_sum = DimeFund.objects.filter(rebalance_date=period_start_date).aggregate(Sum('market_cap'))

        dimeFunds = DimeFund.objects.filter(rebalance_date=period_start_date).order_by('-market_cap')
        for dimeFund in dimeFunds:

            try:
                coin_class = apps.get_model(app_label='DimeCoins', model_name=dimeFund.currency.symbol)
            except:
                print("failed getting class")
                continue

            try:
                xchange_model = apps.get_model('DimeCoins', 'Xchange')
                xchange_mod = xchange_model.objects.using('coins').get(pk=xchange.pk)
                coin = coin_class.objects.using('coins').get(time=int(calendar.timegm(period_start_date.timetuple())),
                                                             xchange=xchange_mod)
            except ObjectDoesNotExist as error:
                print("symbol: {0} for time: {1}: not found : {2}".format(dimeFund.currency.symbol,
                                                                          calendar.timegm(period_start_date.timetuple()),
                                                                          error))
                return
            except TypeError as error:
                print(error)
                return
            rebalance_price[dimeFund.currency.pk] = coin.close
            market_cap[coin.pk] = coin.market_cap

        rank = 1

        for dimeFund in dimeFunds:
            dimeFund.level = level
            dimeFund.rebalance_price = rebalance_price[dimeFund.currency.pk]
            dimeFund.percent_of_dime = dimeFund.market_cap / market_cap_sum['market_cap__sum'] * 100.0
            dimeFund.amount = (dimeFund.percent_of_dime / 100.0 * dimeFund.level) / dimeFund.rebalance_price
            dimeFund.rebalance_value = dimeFund.rebalance_price * dimeFund.amount
            xchange_model = apps.get_model('DimeCoins', 'Xchange')
            xchange_coins = xchange_model.objects.using('coins').get(pk=xchange.pk)

            currency_model = apps.get_model('DimeCoins', dimeFund.currency.symbol.upper())
            try:
                currency = currency_model.objects.using('coins').get(xchange=xchange_coins, time=int(calendar.timegm(period_end_date.timetuple())))
            except ObjectDoesNotExist as error:
                print("symbol: {0}: time: {1}: error:{2}".format(dimeFund.currency.symbol.upper(), calendar.timegm(period_end_date.timetuple()), error))
                return
            except:
                print("symbol: {0}: time: {1}".format(dimeFund.currency.symbol.upper(),
                                                                 calendar.timegm(period_end_date.timetuple())))
                return

            dimeFund.end_price = currency.close
            dimeFund.end_value = dimeFund.end_price * dimeFund.amount
            dimeFund.rank = rank
            rank = rank + 1
            dimeFund.save()

    def verify(self, period, xchange):

        try:
            records = len(DimeFund.objects.filter(period__pk=period.pk))
            if records == 10:
                return True
        except:
            print("failed len of period")

        topCoins_model = apps.get_model('DimeCoins', 'TopCoins')
        topCoins = topCoins_model.objects.using('coins').filter(time=int(calendar.timegm(period.start_date.timetuple()))).order_by('-market_cap')[:10]

        for idx, topCoin in enumerate(topCoins):
            currency = Currency.objects.get(pk=topCoin.currency.pk)
            new_df = DimeFund()

            if period.pk == 2:
                new_df.rebalance_price = topCoin.price
            new_df.period = period
            new_df.rank = idx
            new_df.total_supply = topCoin.total_supply
            new_df.market_cap = topCoin.market_cap
            new_df.currency = currency
            new_df.rebalance_date = period.start_date
            new_df.save()
        return True
