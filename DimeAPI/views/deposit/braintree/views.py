from DimeAPI.settings.base import DEPOSIT_TYPE, DEPOSIT_STATUS, PAYMENT_GATEWAYS, WITHDRAW_STATUS, WITHDRAW_TYPE
from DimeAPI.models import BraintreePaypalTransaction, BraintreeVisaMCTransaction, \
    PaymentGateway, DepositTransaction, DepositTransactionStatus, DepositTransactionType, \
    WithdrawTransaction
from DimeAPI.serializer import BraintreePaypalTransactionSerializer, BraintreeVisaMCTransactionSerializer
from DimeAPI.classes import ReturnResponse
from django.http import JsonResponse
from DimeAPI.classes.PaymentProcessors import BrainTreeProcessor
from DimeAPI.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import views
import logging


logger = logging.getLogger(__name__)


class BraintreeDepositToken(views.APIView):
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        braintree = BrainTreeProcessor.BraintreeGateway()
        token = braintree.getToken()
        return JsonResponse({"token": token}, safe=False)


class BraintreeDepositPaypalTransaction(views.APIView):
    permission_classes = (IsAuthenticated,)
    model = BraintreePaypalTransaction
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        try:
            braintree_paypal_transaction = BraintreePaypalTransactionSerializer(data=request.data)
        except Exception as error:
            return Response(ReturnResponse.Response(1, __name__, 'failed', error).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            braintree_paypal_transaction.is_valid(raise_exception=True)
            instance = braintree_paypal_transaction.save(user_profile=request.user.user_profile)
            braintree = BrainTreeProcessor.BraintreeGateway()
            result = braintree.depositPaypal(instance)
            deposit_transaction = DepositTransaction(user_profile=request.user.user_profile,
                                                     deposit_status=DepositTransactionStatus.objects.get(pk=DEPOSIT_STATUS['SETTLED']),
                                                     payment_gateway=PaymentGateway.objects.get(pk=PAYMENT_GATEWAYS['BRAINTREE']),
                                                     deposit_type=DepositTransactionType.objects.get(pk=DEPOSIT_TYPE['PAYPAL']),
                                                     deposit_id=instance.id)
            deposit_transaction.save()
        except Exception as error:
            return Response(ReturnResponse.Response(1, __name__, 'failed', error).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(ReturnResponse.Response(1, __name__, 'success', result).return_json(),
                        status=status.HTTP_200_OK)


class BraintreeDepositVisaMCTransaction(views.APIView):
    permission_classes = (IsAuthenticated,)
    model = BraintreeVisaMCTransaction
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        try:
            braintree_visamc_transaction = BraintreeVisaMCTransactionSerializer(data=request.data)
        except Exception as error:
            return Response(ReturnResponse.Response(1, __name__, 'failed', error).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            braintree_visamc_transaction.is_valid(raise_exception=True)
            instance = braintree_visamc_transaction.save(user_profile=request.user.user_profile)
            braintree = BrainTreeProcessor.BraintreeGateway()
            result = braintree.depositVisaMC(instance)

            deposit_transaction = DepositTransaction(user_profile=request.user.user_profile,
                                                     deposit_status=DepositTransactionStatus.objects.get(pk=DEPOSIT_STATUS['SETTLED']),
                                                     payment_gateway=PaymentGateway.objects.get(pk=PAYMENT_GATEWAYS['BRAINTREE']),
                                                     deposit_type=DepositTransactionType.objects.get(pk=DEPOSIT_TYPE['VISA']),
                                                     deposit_id=instance.id)
            deposit_transaction.save()
        except Exception as error:
            return Response(ReturnResponse.Response(1, __name__, 'failed', error).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(ReturnResponse.Response(1, __name__, 'success', result).return_json(),
                        status=status.HTTP_200_OK)


class BraintreeWithdrawToken(views.APIView):
    permission_classes = (AllowAny,)
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
        try:
            braintree_paypal_transaction = BraintreePaypalTransactionSerializer(data=request.data)
        except Exception as error:
            return Response(ReturnResponse.Response(1, __name__, 'failed', error).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            braintree_paypal_transaction.is_valid(raise_exception=True)
            instance = braintree_paypal_transaction.save(user_profile=request.user.user_profile)
            braintree = BrainTreeProcessor.BraintreeGateway()
            result = braintree.withdrawPaypal(instance)
            deposit_transaction = WithdrawTransaction(user_profile=request.user.user_profile,
                                                     deposit_status=DepositTransactionStatus.objects.get(pk=WITHDRAW_STATUS['SETTLED']),
                                                     payment_gateway=PaymentGateway.objects.get(pk=PAYMENT_GATEWAYS['BRAINTREE']),
                                                     deposit_type=DepositTransactionType.objects.get(pk=WITHDRAW_TYPE['PAYPAL']),
                                                     deposit_id=instance.id)
            deposit_transaction.save()
        except Exception as error:
            return Response(ReturnResponse.Response(1, __name__, 'failed', error).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(ReturnResponse.Response(1, __name__, 'success', result).return_json(),
                        status=status.HTTP_200_OK)


class BraintreeWithdrawVisaMCTransaction(views.APIView):
    permission_classes = (IsAuthenticated,)
    model = BraintreeVisaMCTransaction
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    def post(self, request, *args, **kwargs):
        try:
            braintree_visamc_transaction = BraintreeVisaMCTransactionSerializer(data=request.data)
        except Exception as error:
            return Response(ReturnResponse.Response(1, __name__, 'failed', error).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            braintree_visamc_transaction.is_valid(raise_exception=True)
            instance = braintree_visamc_transaction.save(user_profile=request.user.user_profile)
            braintree = BrainTreeProcessor.BraintreeGateway()
            result = braintree.withdrawVisaMC(instance)

            deposit_transaction = WithdrawTransaction(user_profile=request.user.user_profile,
                                                     deposit_status=DepositTransactionStatus.objects.get(pk=DEPOSIT_STATUS['SETTLED']),
                                                     payment_gateway=PaymentGateway.objects.get(pk=PAYMENT_GATEWAYS['BRAINTREE']),
                                                     deposit_type=DepositTransactionType.objects.get(pk=DEPOSIT_TYPE['VISA']),
                                                     deposit_id=instance.id)
            deposit_transaction.save()
        except Exception as error:
            return Response(ReturnResponse.Response(1, __name__, 'failed', error).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(ReturnResponse.Response(1, __name__, 'success', result).return_json(),
                        status=status.HTTP_200_OK)
