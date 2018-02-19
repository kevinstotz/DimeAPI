from __future__ import unicode_literals
from django.db import models
from DimeAPI.models import Xchange
from DimeAPI.settings.base import COIN_SYMBOL_LENGTH


class Currency2(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=COIN_SYMBOL_LENGTH, default="")
    objects = models.Manager()

    class Meta:
        managed = False


class Coin(models.Model):
    id = models.AutoField(primary_key=True)
    xchange = models.ForeignKey(Xchange, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency2, on_delete=models.CASCADE)
    time = models.BigIntegerField(verbose_name="Date of Price", default=0)
    open = models.FloatField(default=0.0)
    close = models.FloatField(default=0.0)
    high = models.FloatField(default=0.0)
    low = models.FloatField(default=0.0)
    volume = models.FloatField(default=0.0)
    market_cap = models.FloatField(default=0.0)
    objects = models.Manager()

    class Meta:
        abstract = True
        managed = False


class ADA(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class BCH(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class BTC(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class BTG(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class DASH(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class DOGE(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class DSH(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class ETC(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class ETH(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class EOS(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class ICN(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class IOTA(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class LSK(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class LTC(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class MAID(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class MIOTA(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class NEO(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class OMGC(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class REP(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class STEEM(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class WAVES(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class XEM(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class XLM(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class XMR(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class XRP(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'


class ZEC(Coin):
    pass

    class Meta:
        managed = False,
        app_label = 'dimecoins'
