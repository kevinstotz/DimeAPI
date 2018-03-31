from DimeAPI.models import Fund, FundCurrency, ContactUsForm, NewsLetter
from DimeAPI.serializer import ContactUsFormSerializer, NewsLetterSerializer, Currency
from DimeAPI.settings.base import XCHANGE
from DimeAPI.classes import ReturnResponse, MyEmail, NewsFeed
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import json
import logging


logger = logging.getLogger(__name__)


class NewsLetterSubscribe(generics.GenericAPIView):
    model = NewsLetter
    permission_classes = (AllowAny, )
    serializer_class = NewsLetterSerializer
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    queryset = NewsLetter.objects.all()

    def post(self, request):
        news_letter = ""

        if NewsLetter.objects.filter(email=request.data['email']).exists():
            result = "Email exists."
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, "Subscription Failed", result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            news_letter = NewsLetterSerializer(data=request.data, many=False, partial=True)
            news_letter.is_valid(raise_exception=True)
        except Exception as error:
            result = 'Failed to parse JSON:{0}:{1}'.format(request, error)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, "Subscription Failed", result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        news_letter.save()
        result = "Joined Mailing List"
        logger.error(result + request.data['email'])
        return Response(ReturnResponse.Response(0, __name__, "Subscription Successful", result).return_json(),
                        status=status.HTTP_201_CREATED)


class CoinNews(generics.ListAPIView):
    model = Fund
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        try:
            fund = Fund.objects.get(pk=self.kwargs['pk'])
        except Exception as error:
            return Response(ReturnResponse.Response(1, __name__, "Invalid Fund", error).return_json(), status=status.HTTP_200_OK)
        try:
            fundCurrency = FundCurrency.objects.filter(fund=fund).order_by('-rebalance__pk')[0:1].get()
        except Exception as error:
            return Response(ReturnResponse.Response(2, __name__, "Invalid FundCurrency", error).return_json(), status=status.HTTP_200_OK)


        news = []
        newsfeed = NewsFeed.NewsFeed(XCHANGE['CRYPTOPANIC'])
        for record in FundCurrency.objects.filter(fund=fund).order_by('-rebalance__pk')[:fundCurrency.rebalance.num_of_coins]:
            try:
                currency = Currency.objects.using('coins').get(pk=record.currency)
            except Exception as error:
                print(error)
                return Response(ReturnResponse.Response(3, __name__, "No currency", error).return_json(),
                                status=status.HTTP_200_OK)
            news.append(newsfeed.get_news_feed(currency.symbol))
        return Response(ReturnResponse.Response(0, __name__, json.dumps(news), 0).return_json(),
                        status=status.HTTP_200_OK)


class ContactUs(generics.CreateAPIView):
    queryset = ContactUsForm.objects.all()
    serializer_class = ContactUsFormSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        contact_us = ''
        try:
            contact_us = ContactUsFormSerializer(data=request.data, partial=True)
            contact_us.is_valid(raise_exception=True)
        except Exception as error:
            result = 'Failed to parse JSON:{0}'.format(request) + contact_us + str(error)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, "Contact Us send Failed", result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        contact_us.create(contact_us.validated_data)
        my_email = MyEmail.MyEmail(name=contact_us.validated_data['name'])
        my_email.send_contact_us(contact_us)
        result = "Email Sent!"
        logger.error(result)
        return Response(ReturnResponse.Response(0, __name__, result, 0).return_json(),
                        status=status.HTTP_201_CREATED)


class IndexPage(generics.ListAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

