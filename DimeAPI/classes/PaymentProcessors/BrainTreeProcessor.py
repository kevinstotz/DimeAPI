import braintree
import logging
from DimeAPI.models import PaymentGateway
from DimeAPI.settings.base import PAYMENT_GATEWAYS
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)


class BraintreeGateway:

    def __init__(self):
        #  instance variable unique to each instance
        try:
            self.payment_gateway = PaymentGateway.objects.get(pk=PAYMENT_GATEWAYS['BRAINTREE'])
        except ObjectDoesNotExist as error:
            logger.error(error)
            return
        self.merchant_id = self.payment_gateway.merchant_id
        self.public_key = self.payment_gateway.public_key
        self.private_key = self.payment_gateway.private_key
        self.gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                environment=braintree.Environment.Sandbox,
                merchant_id=self.merchant_id,
                public_key=self.public_key,
                private_key=self.private_key
            )
        )

    def getToken(self):
        clientToken = self.gateway.client_token.generate();
        return clientToken

    def depositPaypal(self, braintree_paypal_transaction):
        result = self.gateway.transaction.sale({
            "amount": str(braintree_paypal_transaction.amount),
            "payment_method_nonce" : braintree_paypal_transaction.nonce,
            "order_id": str(braintree_paypal_transaction.id),
            "options": {
                "submit_for_settlement": True,
                "paypal": {
                    "custom_field": "PayPal custom field",
                    "description": "Description for PayPal email receipt",
              },
            },
        })
        if result.is_success:
            logger.info(result)
            return result.transaction.id
        else:
            logger.error(result)
            return result

    def depositVisaMC(self, braintree_VisaMC_transaction):
        result = self.gateway.transaction.sale({
            "amount": str(braintree_VisaMC_transaction.amount),
            "payment_method_nonce": braintree_VisaMC_transaction.nonce,
            "order_id": str(braintree_VisaMC_transaction.id),
            "options": {
                "submit_for_settlement": True
            },
        })
        if result.is_success:
            logger.info(result)
            return result.transaction.id
        else:
            logger.error(result)
            return result

    def withdrawPaypal(self, braintree_paypal_transaction):
        result = self.gateway.transaction.sale({
            "amount": str(braintree_paypal_transaction.amount),
            "payment_method_nonce": braintree_paypal_transaction.nonce,
            "order_id": str(braintree_paypal_transaction.id),
            "options": {
                "submit_for_settlement": True,
                "paypal": {
                    "custom_field": "PayPal custom field",
                    "description": "Description for PayPal email receipt",
              },
            },
        })
        if result.is_success:
            logger.info(result)
            return result.transaction.id
        else:
            logger.info(result)
            return result

    def withdrawVisaMC(self, braintree_VisaMC_transaction):
        result = self.gateway.transaction.sale({
            "amount": str(braintree_VisaMC_transaction.amount),
            "payment_method_nonce": braintree_VisaMC_transaction.nonce,
            "order_id": str(braintree_VisaMC_transaction.id),
            "options": {
                "submit_for_settlement": True
            },
        })
        if result.is_success:
            logger.info(result)
            return result.transaction.id
        else:
            logger.info(result)
            return result