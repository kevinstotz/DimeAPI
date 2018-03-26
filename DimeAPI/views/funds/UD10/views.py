from DimeAPI.settings.base import XCHANGE
from DimeAPI.models import UD10Fund, UD10History, UD10Period
from DimeAPI.serializer import UD10TableChartSerializer, UD10HistorySerializer, UD10PieChartSerializer, \
    UD10RebalanceDateValueSerializer, UD10TableListChartSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser


class UD10LineChart(generics.ListAPIView):
    model = UD10History
    serializer_class = UD10HistorySerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = UD10History.objects.all().filter(xchange=XCHANGE['COIN_MARKET_CAP'])
    filter_backends = (DjangoFilterBackend,)
    ordering = ('name',)
    filter_fields = ('xchange',)


class UD10RebalanceDateValue(generics.ListAPIView):
    model = UD10Period
    serializer_class = UD10RebalanceDateValueSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = UD10Period.objects.all()[1:]


class UD10PieChart(generics.ListAPIView):
    model = UD10Fund
    serializer_class = UD10PieChartSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = UD10Fund.objects.filter(rebalance_date='2018-02-23')


class UD10TableChart(generics.ListAPIView):
    model = UD10Fund
    serializer_class = UD10TableChartSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = UD10Fund.objects.filter(rebalance_date='2018-02-23')


class UD10TableListChart(generics.ListAPIView):
    model = UD10Fund
    serializer_class = UD10TableListChartSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = UD10Fund.objects.filter(rebalance_date='2018-02-23')
