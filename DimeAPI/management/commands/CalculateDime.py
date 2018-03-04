from django.core.exceptions import ObjectDoesNotExist
from DimeAPI.models import Xchange, DimeMutualFund, Period
from django.core.management.base import BaseCommand
from DimeAPI.settings.base import XCHANGE
from datetime import datetime, timedelta
import calendar
from django.apps import apps
from django.db.models import Sum


class Command(BaseCommand):

    def handle(self, *args, **options):
        periods = Period.objects.all()[1:]
        xchange = Xchange.objects.get(pk=XCHANGE['COIN_MARKET_CAP'])

        for period in periods:
            self.calculateDime(period, xchange)

    def calculateDime(self, period, xchange):

        period_start_date = str(period.start_year) + "-" + str(period.start_month) + "-" + str(period.start_day)
        period_start_date = datetime.strptime(period_start_date, '%Y-%m-%d')

        period_end_date = str(period.end_year) + "-" + str(period.end_month) + "-" + str(period.end_day)
        period_end_date = datetime.strptime(period_end_date, '%Y-%m-%d')

        prior_DimeMutualFund_Value = DimeMutualFund.objects.filter(period__pk=(period.pk-1)).aggregate(Sum('end_value'))
        if period.pk == 1:
            level = 10
        else:
            level = prior_DimeMutualFund_Value['end_value__sum']

        if period_start_date > datetime.utcnow():
            return

        if period_end_date > datetime.utcnow():
            period_end_date = period_end_date.utcnow().replace(second=0, minute=0, hour=0)
            period_end_date = period_end_date - timedelta(days=2)

        dimeMutualFunds = DimeMutualFund.objects.filter(rebalance_date=period_start_date).order_by('-market_cap')

        market_cap = dict()
        for dimeMutualFund in dimeMutualFunds:

            try:
                coin_class = apps.get_model(app_label='DimeCoins', model_name=dimeMutualFund.currency.symbol)
            except:
                print("failed getting class")
                continue

            try:
                xchange_model = apps.get_model('DimeCoins', 'Xchange')
                xchange_mod = xchange_model.objects.using('coins').get(pk=xchange.pk)
                coin = coin_class.objects.using('coins').get(time=int(calendar.timegm(period_start_date.timetuple())),
                                                              xchange=xchange_mod)
            except ObjectDoesNotExist as error:
                print("symbol: {0} for time: {1}: not found : {2}".format(dimeMutualFund.currency.symbol,
                                                                          calendar.timegm(period_start_date.timetuple()),
                                                                          error))
                return
            except TypeError as error:
                print(error)
                return
            market_cap[dimeMutualFund.pk] = coin.market_cap

        rank = 1

        for dimeMutualFund in dimeMutualFunds:
            dimeMutualFund.level = level
            dimeMutualFund.percent_of_dime = market_cap[dimeMutualFund.pk] / sum(market_cap.values()) * 100.0
            dimeMutualFund.amount = (dimeMutualFund.percent_of_dime / 100.0 * dimeMutualFund.level) / dimeMutualFund.rebalance_price
            dimeMutualFund.rebalance_value = dimeMutualFund.rebalance_price * dimeMutualFund.amount
            xchange_model = apps.get_model('DimeCoins', 'Xchange')
            xchange_coins = xchange_model.objects.using('coins').get(pk=xchange.pk)

            currency_model = apps.get_model('DimeCoins', dimeMutualFund.currency.symbol.upper())
            currency = currency_model.objects.using('coins').get(xchange=xchange_coins, time=int(calendar.timegm(period_start_date.timetuple())))

            dimeMutualFund.rebalance_price = currency.close
            try:
                currency = currency_model.objects.using('coins').get(xchange=xchange_coins, time=int(calendar.timegm(period_end_date.timetuple())))
            except ObjectDoesNotExist as error:
                print("symbol: {0}: time: {1}: error:{2}".format(currency.currency.symbol, calendar.timegm(period_end_date.timetuple()), error))
                return

            dimeMutualFund.end_price = currency.close
            dimeMutualFund.end_value = dimeMutualFund.end_price * dimeMutualFund.amount
            dimeMutualFund.rank = rank
            rank = rank + 1
            dimeMutualFund.save()