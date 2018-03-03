from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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
            self.calculateDimeIndex(period, xchange)

    def calculateDimeIndex(self, period, xchange):

        period_start_date = str(period.start_year) + "-" + str(period.start_month) + "-" + str(period.start_day)
        period_start_date = datetime.strptime(period_start_date, '%Y-%m-%d')

        period_end_date = str(period.end_year) + "-" + str(period.end_month) + "-" + str(period.end_day)
        period_end_date = datetime.strptime(period_end_date, '%Y-%m-%d')

        if period_start_date > datetime.utcnow():
            return

        if period_end_date > datetime.utcnow():
            #  period_end_date = datetime.utcnow()
            period_end_date = period_end_date.utcnow().replace(second=0, minute=0, hour=0)
            period_end_date = period_end_date - timedelta(days=1)

        prior_period = Period.objects.get(pk=(period.pk - 1))

        prior_period_start_date = str(prior_period.start_year) + "-" + str(prior_period.start_month) + "-" + str(
            prior_period.start_day)
        prior_period_start_date = datetime.strptime(prior_period_start_date, '%Y-%m-%d')

        total_cap_market_sum = DimeMutualFund.objects.filter(rebalance_date=period_start_date).aggregate(
            value=Sum('market_cap'))
        index_value = DimeMutualFund.objects.filter(rebalance_date=prior_period_start_date).aggregate(
            value=Sum('end_value'))
        dimeMutualFunds = DimeMutualFund.objects.filter(rebalance_date=period_start_date).order_by('-market_cap')
        rank = 1

        for dimeMutualFund in dimeMutualFunds:
            if period.pk == 1:
                dimeMutualFund.level = 10
            else:
                dimeMutualFund.level = index_value['value']

            dimeMutualFund.percent_of_dime = dimeMutualFund.market_cap / total_cap_market_sum['value'] * 100.0
            dimeMutualFund.amount = (dimeMutualFund.percent_of_dime / 100.0 * dimeMutualFund.level) / dimeMutualFund.rebalance_price
            dimeMutualFund.rebalance_value = dimeMutualFund.rebalance_price * dimeMutualFund.amount
            xchange_model = apps.get_model('DimeCoins', 'Xchange')
            xchange_coins = xchange_model.objects.using('coins').get(pk=xchange.pk)

            currency_model = apps.get_model('DimeCoins', dimeMutualFund.currency.symbol.upper())
            currency = currency_model.objects.using('coins').get(xchange=xchange_coins, time=int(calendar.timegm(period_start_date.timetuple())))

            dimeMutualFund.rebalance_price = currency.close
            currency = currency_model.objects.using('coins').get(xchange=xchange_coins, time=int(calendar.timegm(period_end_date.timetuple())))

            dimeMutualFund.end_price = currency.close
            dimeMutualFund.end_value = dimeMutualFund.end_price * dimeMutualFund.amount
            dimeMutualFund.rank = rank
            rank = rank + 1
            dimeMutualFund.save()