from DimeAPI.models import NewsLetter, BraintreePaypalTransaction, BraintreeVisaMCTransaction
from DimeAPI.classes.PaymentProcessors import BrainTreeProcessor
from DimeAPI.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework import views
from django.http import JsonResponse
import logging


logger = logging.getLogger(__name__)


class BraintreeWithdrawToken(views.APIView):
    permission_classes = (AllowAny,)
    model = NewsLetter
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        braintree = BrainTreeProcessor.BraintreeGateway()
        token = braintree.getToken()
        return JsonResponse({"token": token}, safe=False)


class BraintreeWithdrawPaypalTransaction(views.APIView):
    permission_classes = (IsAuthenticated,)
    model = BraintreePaypalTransaction
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        pass


class BraintreeWithdrawVisaMCTransaction(views.APIView):
    permission_classes = (IsAuthenticated,)
    model = BraintreeVisaMCTransaction
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        pass

