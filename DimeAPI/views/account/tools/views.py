from DimeAPI.models import Country, State, City, ZipCode
from DimeAPI.serializer import CountrySerializer
from DimeAPI.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.parsers import JSONParser
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')


class CountryView(generics.ListAPIView):
    model = Country
    serializer_class = CountrySerializer
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    queryset = Country.objects.all().order_by('name')


class CityView(generics.ListAPIView):
    model = City
    serializer_class = CountrySerializer
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    queryset = City.objects.all().order_by('name')

    def get_queryset(self):
        state = self.kwargs['State']
        return City.objects.filter(state__pk=state)


class StateView(generics.ListAPIView):
    model = State
    serializer_class = CountrySerializer
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    queryset = State.objects.all().order_by('name')

    def get_queryset(self):
        country = self.kwargs['Country']
        return State.objects.filter(country__pk=country)


class ZipCodeView(generics.ListAPIView):
    model = ZipCode
    serializer_class = CountrySerializer
    parser_classes = (JSONParser,)
    permission_classes = (IsAuthenticated,)
    queryset = ZipCode.objects.all().order_by('zip_code')

    def get_queryset(self):
        city = self.kwargs['City']
        return ZipCode.objects.filter(city__pk=city)
