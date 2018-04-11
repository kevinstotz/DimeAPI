from DimeAPI.serializer import CoinSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser


class CoinList(generics.ListAPIView):
    serializer_class = CoinSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)

