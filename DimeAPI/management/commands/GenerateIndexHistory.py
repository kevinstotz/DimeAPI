from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from DimeAPI.models import Xchange, DimeMutualFund, Period, DimeHistory
from django.core.management.base import BaseCommand
from DimeAPI.settings.base import XCHANGE
from datetime import datetime, timedelta
import calendar
from django.apps import apps


class Command(BaseCommand):

    def handle(self, *args, **options):

        values = dict()
        periods = Period.objects.all()[1:]
        for period in periods:
            start_date = datetime.strptime(str(period.start_year) + '-' + str(period.start_month) + '-' + str(period.start_day), '%Y-%m-%d').date()
            rebalance_date = start_date

            end_date = datetime.strptime(str(period.end_year) + '-' + str(period.end_month) + '-' + str(period.end_day), '%Y-%m-%d').date()
            if end_date > datetime.utcnow().date():
                end_date = datetime.utcnow().date()
            while start_date < end_date:

                dimeindex = DimeMutualFund.objects.filter(rebalance_date=rebalance_date)
                running_total = 0
                for coin in dimeindex:
                    coin_class = apps.get_model(app_label='DimeCoins', model_name=coin.currency.symbol)
                    try:
                        xchange_model = apps.get_model('DimeCoins', 'Xchange')
                        xchange_mod = xchange_model.objects.using('coins').get(pk=XCHANGE['COIN_MARKET_CAP'])
                        index = coin_class.objects.using('coins').get(time=int(calendar.timegm(start_date.timetuple())), xchange=xchange_mod)
                    except ObjectDoesNotExist as error:
                        print(error)
                        return
                    except TypeError as error:
                        print(error)
                        return

                    running_total = running_total + coin.amount * index.close
                xchange = Xchange.objects.get(pk=XCHANGE['COIN_MARKET_CAP'])
                try:
                    dimeHistory = DimeHistory.objects.get(time=int(calendar.timegm(start_date.timetuple())), xchange=xchange)
                    dimeHistory.save()
                except ObjectDoesNotExist:
                    dimeHistory = DimeHistory(time=int(calendar.timegm(start_date.timetuple())), xchange=xchange)
                    dimeHistory.value = running_total
                    dimeHistory.save()
                    
                except MultipleObjectsReturned:
                    print("found multiple entries for: {0} {1}".format(int(calendar.timegm(start_date.timetuple())), xchange.pk ))
                    continue

                start_date = start_date + timedelta(days=1)
        return