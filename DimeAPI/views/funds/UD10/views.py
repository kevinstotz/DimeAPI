from DimeAPI.models import Fund, FundHistory, FundRebalanceDate, FundCurrency
from DimeAPI.serializer import FundTableChartSerializer, FundLineChartSerializer, FundPieChartSerializer, \
    FundRebalanceDateValueSerializer, FundTableListChartSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser


class FundLineChart(generics.ListAPIView):
    model = FundHistory
    serializer_class = FundLineChartSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = FundHistory.objects.all()
    filter_backends = (DjangoFilterBackend,)
    ordering = ('name',)

    def get_queryset(self):
        try:
            fund = Fund.objects.get(pk=self.kwargs['pk'])
            return FundHistory.objects.filter(fund=fund).order_by('time')
        except Exception as error:
            print(error)
            return


class FundRebalanceDateValue(generics.ListAPIView):
    model = FundRebalanceDate
    serializer_class = FundRebalanceDateValueSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = FundRebalanceDate.objects.all()

    def get_queryset(self):
        try:
            fund = Fund.objects.get(pk=self.kwargs['pk'])
            return FundRebalanceDate.objects.filter(fund=fund).order_by('+start_date')
        except Exception as error:
            print(error)
            return



class FundPieChart(generics.ListAPIView):
    model = FundCurrency
    serializer_class = FundPieChartSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = FundCurrency.objects.all()

    def get_queryset(self):
        try:
            fund = Fund.objects.get(pk=self.kwargs['pk'])
            rebalance_date = FundRebalanceDate.objects.filter(fund=fund).order_by('start_date')[0:1].get()
            return FundCurrency.objects.all().filter(fund=fund).order_by('-rebalance__start_date')[:rebalance_date.num_of_coins]
        except Exception as error:
            print(error)
            return


class FundTableChart(generics.ListAPIView):
    model = FundCurrency
    serializer_class = FundTableChartSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = FundCurrency.objects.all()

    def get_queryset(self):
        try:
            fund = Fund.objects.get(pk=self.kwargs['pk'])
            rebalance_date = FundRebalanceDate.objects.filter(fund=fund).order_by('start_date')[0:1].get()
            return FundCurrency.objects.all().filter(fund=fund).order_by('-rebalance__start_date')[:rebalance_date.num_of_coins]
        except Exception as error:
            print(error)
            return


class FundTableListChart(generics.ListAPIView):
    model = FundCurrency
    serializer_class = FundTableListChartSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = FundCurrency.objects.all()

    def get_queryset(self):
        try:
            fund = Fund.objects.get(pk=self.kwargs['pk'])
            return FundCurrency.objects.all().filter(fund=fund).order_by('-rebalance__start_date')[:10]
        except Exception as error:
            print(error)
            return