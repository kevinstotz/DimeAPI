

class ADA(Coin):
    pass


class BCH(Coin):
    pass


class BTC(Coin):
    pass


class BTG(Coin):
    pass


class CRIX(Coin):
    pass


class DASH(Coin):
    pass


class DOGE(Coin):
    pass


class DSH(Coin):
    pass


class EOS(Coin):
    pass


class ETC(Coin):
    pass


class ETH(Coin):
    pass


class ICN(Coin):
    pass


class IOTA(Coin):
    pass


class LSK(Coin):
    pass


class LTC(Coin):
    pass


class MAID(Coin):
    pass


class MIOTA(Coin):
    pass


class NEO(Coin):
    pass


class OMGC(Coin):
    pass


class REP(Coin):
    pass


class STEEM(Coin):
    pass


class WAVES(Coin):
    pass


class XEM(Coin):
    pass


class XLM(Coin):
    pass


class XMR(Coin):
    pass


class XRP(Coin):
    pass


class ZEC(Coin):
    pass
	
	       if self.symbol == 'ADA':
            try:
                return ADA.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return ADA()

        if self.symbol == 'BCH':
            try:
                return BCH.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return BCH()

        if self.symbol == 'BTC':
            try:
                return BTC.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return BTC()

        if self.symbol == 'BTG':
            try:
                return BTG.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return BTG()

        if self.symbol == 'CRIX':
            try:
                return CRIX.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return CRIX()

        if self.symbol == 'DASH':
            try:
                return DASH.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return DASH()

        if self.symbol == 'DOGE':
            try:
                return DOGE.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return DOGE()

        if self.symbol == 'DSH':
            try:
                return DSH.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return DSH()

        if self.symbol == 'EOS':
            try:
                return EOS.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return EOS()

        if self.symbol == 'ETH':
            try:
                return ETH.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return ETH()

        if self.symbol == 'ETC':
            try:
                return ETC.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return ETC()

        if self.symbol == 'ICN':
            try:
                return ICN.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return ICN()

        if self.symbol == 'LTC':
            try:
                return LTC.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return LTC()

        if self.symbol == 'LSK':
            try:
                return LSK.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return LSK()

        if self.symbol == 'MAID':
            try:
                return MAID.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return MAID()

        if self.symbol == 'MIOTA':
            try:
                return MIOTA.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return MIOTA()

        if self.symbol == 'IOTA':
            try:
                return IOTA.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return IOTA()

        if self.symbol == 'NEO':
            try:
                return NEO.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return NEO()

        if self.symbol == 'OMGC':
            try:
                return OMGC.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return OMGC()

        if self.symbol == 'REP':
            try:
                return REP.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return REP()

        if self.symbol == 'STEEM':
            try:
                return STEEM.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return STEEM()

        if self.symbol == 'WAVES':
            try:
                return WAVES.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return WAVES()

        if self.symbol == 'XEM':
            try:
                return XEM.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return XEM()

        if self.symbol == 'XMR':
            try:
                return XMR.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return XMR()

        if self.symbol == 'XRP':
            try:
                return XRP.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return XRP()

        if self.symbol == 'ZEC':
            try:
                return ZEC.objects.get(time=time, xchange=exchange)
            except ObjectDoesNotExist:
                return ZEC()

