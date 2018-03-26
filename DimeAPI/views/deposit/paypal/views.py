from DimeAPI.models import PaypalTransaction
from DimeAPI.serializer import PaypalTransactionSerializer
from DimeAPI.classes import ReturnResponse
from DimeAPI.classes.PaymentProcessors import PayPalProcessor
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import views
import logging


logger = logging.getLogger(__name__)


class PaypalCreate(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        pp = PayPalProcessor.PayPalProcessor()
        pp.createPayment()
        logger.info("Paypal payment created")
        return Response(ReturnResponse.Response(0, __name__, 'success', "0").return_json(),
                        status=status.HTTP_201_CREATED)


class PaypalCapture(views.APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
    model = PaypalTransaction
    serializer_class = PaypalTransactionSerializer

    def post(self, request, *args, **kwargs):
        pp = PayPalProcessor.PayPalProcessor()
        try:
            serializer = PaypalTransactionSerializer(data=request.data)
        except Exception as error:
            logger.error("Paypal payment captured error: " + error)
            return
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as error:
            logger.error("Paypal payment captured error: " + error)
            return Response(ReturnResponse.Response(1, __name__, 'failed', error).return_json(),
                        status=status.HTTP_200_OK)

        pp.capture(serializer)

        return Response(ReturnResponse.Response(0, __name__, 'success', "0").return_json(),
                        status=status.HTTP_200_OK)


class PaypalReturn(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logger.info("Paypal payment returned")
        return Response(ReturnResponse.Response(0, __name__, 'success', 0).return_json(),
                        status=status.HTTP_201_CREATED)

