import paypalrestsdk
from DimeAPI.settings.base import PAYMENT_GATEWAYS, PAYPAL_RETURN_URL, PAYPAL_CANCEL_URL
from django.core.exceptions import ObjectDoesNotExist
from DimeAPI.models import PaymentGateway
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')


class PayPalProcessor:

    def __init__(self):
        #  instance variable unique to each instance
        try:
            self.payment_gateway = PaymentGateway.objects.get(pk=PAYMENT_GATEWAYS['PAYPAL'])
        except ObjectDoesNotExist as error:
            logging.error('{0}'.format(error))
            return
        self.client_id = self.payment_gateway.client_id
        self.client_secret = self.payment_gateway.client_secret
        self.paypal_mode = self.payment_gateway.environment
        self.return_url = PAYPAL_RETURN_URL
        self.cancel_url = PAYPAL_CANCEL_URL
        self.access_token_url = '/v1/oauth2/token'

        self.payment = paypalrestsdk.configure({
            "mode": self.paypal_mode,
            "client_id": self.client_id,
            "client_secret": self.client_secret})

    def getAccessToken(self):
        try:
            webhook = paypalrestsdk.Webhook.find("82Y00654DD7482205")
            logger.info("Got Details for Webhook[%s]" % webhook.id)
        except paypalrestsdk.ResourceNotFound as error:
            logger.info("Webhook Not Found: {0}".format(error))

    def getEventTypes(self):
        try:
            webhook = paypalrestsdk.Webhook.find("82Y00654DD7482205")
            webhook_event_types = webhook.get_event_types()
            logger.info(webhook_event_types)

        except paypalrestsdk.ResourceNotFound as error:
            logger.info("Webhook Not Found: {0}".format(error))

    def getAllWebHooks(self):
        history = paypalrestsdk.Webhook.all()
        logger.info(history)

        logger.info("List Webhook:")
        for webhook in history:
            logger.info("  -> Webhook[%s]" % webhook.name)

    def capture(self, paypal_transaction):
        try:
            webhook = paypalrestsdk.Webhook.find("82Y00654DD7482205")
            webhook_event_types = webhook.get_event_types()
            logger.info(webhook_event_types)

        except paypalrestsdk.ResourceNotFound as error:
            logger.info("Webhook Not Found: {0}".format(error))

    def createPayment(self, currency="USD", name="Fund", sku=1, price="5.00", quantiity=1):
        self.payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": self.return_url,
                "cancel_url": self.cancel_url},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": name,
                        "sku": sku,
                        "price": price,
                        "currency": currency,
                        "quantity": quantiity}]},
                "amount": {
                    "total": price,
                    "currency": currency},
                "description": "Fund"}]})
        if self.payment.create():
            logger.info("Payment created successfully")
        else:
            logger.info(self.payment.error)

    def postPayment(self):
        self.payment = paypalrestsdk.Payment.find("PAY-57363176S1057143SKE2HO3A")

        if self.payment.execute({"payer_id": "DUFRQ8GWYMJXC"}):
            logger.info("Payment execute successfully")
        else:
            logger.info(self.payment.error)  # Error Hash

    def authorizePayment(self):
        for link in self.payment.links:
            if link.rel == "approval_url":
                # Convert to str to avoid Google App Engine Unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                approval_url = str(link.href)
                logger.info("Redirect for approval: %s" % approval_url)
