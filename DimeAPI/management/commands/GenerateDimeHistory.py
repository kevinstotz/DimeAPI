from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from DimeAPI.models import Xchange, UD10Fund, UD10Period, UD10History
from django.core.management.base import BaseCommand
from DimeAPI.settings.base import XCHANGE
from datetime import datetime, timedelta
import calendar
from django.apps import apps

class Command(BaseCommand):

    def handle(self, *args, **options):

        xchange = Xchange.objects.get(pk=XCHANGE['COIN_MARKET_CAP'])
        periods = UD10Period.objects.all().order_by('start_date')[15:]
        for period in periods:
            start_date = rebalance_date = period.start_date
            end_date = period.end_date

            if end_date > datetime.utcnow().date():
                end_date = datetime.utcnow().date()
            while start_date < end_date:

                ud10Fund = UD10Fund.objects.filter(rebalance_date=rebalance_date)
                running_total = 0.0
                for coin in ud10Fund:
                    try:
                        coin_class = apps.get_model(app_label='DimeCoins', model_name=coin.currency.symbol)
                    except Exception as error:
                        print(error)
                    try:
                        xchange_model = apps.get_model('DimeCoins', 'Xchange')
                        xchange_mod = xchange_model.objects.using('coins').get(pk=xchange.pk)
                        index = coin_class.objects.using('coins').get(time=int(calendar.timegm(start_date.timetuple())), xchange=xchange_mod)
                    except ObjectDoesNotExist as error:
                        print("symbol: {0} for time: {1}: not found : {2}".format(coin.currency.symbol, calendar.timegm(start_date.timetuple()), error))
                        return
                    except TypeError as error:
                        print(error)
                        return

                    running_total = running_total + float(coin.amount) * float(index.close)

                try:
                    ud10History = UD10History.objects.get(time=int(calendar.timegm(start_date.timetuple())), xchange=xchange)
                    ud10History.value = running_total
                    ud10History.save()

                except ObjectDoesNotExist:
                    ud10History = UD10History(time=int(calendar.timegm(start_date.timetuple())), xchange=xchange)
                    ud10History.value = running_total
                    ud10History.save()

                except MultipleObjectsReturned:
                    print("found multiple entries for: {0} {1}".format(int(calendar.timegm(start_date.timetuple())), xchange.pk))
                    continue

                start_date = start_date + timedelta(days=1)
        return
