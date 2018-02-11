import logging
from DimeAPI.models import Network
from web3 import Web3, HTTPProvider
from django.core.exceptions import ObjectDoesNotExist

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


class BlockChainNetwork(object):

    def __init__(self, network_id):

        super(BlockChainNetwork, self).__init__()
        try:
            self.network = Network.objects.get(Number=network_id)
            logging.debug('Created BC : %s', self.network.Number)
        except ObjectDoesNotExist:
            self.network = Network.objects.get(pk=0)
            self.provider = 0
            self.web3 = 0
            logging.debug('Network does not exist in DB:')
        except (RuntimeError, TypeError, NameError):
            self.network = Network.objects.get(pk=0)
            self.provider = 0
            self.web3 = 0
        else:
            self.provider = HTTPProvider(self.network.Url)
            self.web3 = Web3(self.provider)

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            # logging.debug('Running: %s', self.active)

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            # logging.debug('Running: %s', self.active)


