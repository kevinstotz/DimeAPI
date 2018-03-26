from DimeAPI.models import DepositTransaction, WithdrawTransaction
from DimeAPI.serializer import DepositTransactionSerializer, WithdrawTransactionSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser
import logging


logger = logging.getLogger(__name__)

class WithdrawTransactionHistory(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    model = WithdrawTransaction
    serializer_class = WithdrawTransactionSerializer
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    queryset = WithdrawTransaction.objects.all().order_by('inserted')


class DepositTransactionHistory(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    model = DepositTransaction
    serializer_class = DepositTransactionSerializer
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    queryset = DepositTransaction.objects.all().order_by('inserted')

class Balance(generics.ListAPIView):
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    #  serializer_class = Serializer

    def get(self, request, *args, **kwargs):
        pass