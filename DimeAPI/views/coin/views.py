from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser


class CoinList(generics.ListAPIView):
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)

