import logging
import ipfsapi

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )
IPFS_HASH_LENGTH = 46


class IPFS(object):

    def __init__(self, host='127.0.0.1', port=10006):
        super(IPFS, self).__init__()
        self.port = port
        self.host = host
        try:
            self.api = ipfsapi.Client(self.host, self.port)
            logging.debug('Created IPFS Client')
        except Exception:
            logging.debug('Network does not exist: %s', self.host)
