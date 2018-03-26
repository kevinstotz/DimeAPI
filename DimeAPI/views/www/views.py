from DimeAPI.models import UD10Fund, ContactUsForm, NewsLetter
from DimeAPI.serializer import ContactUsFormSerializer, CoinNewsSerializer, NewsLetterSerializer
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
    model = UD10Fund
    serializer_class = CoinNewsSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        newsfeed = NewsFeed.NewsFeed()
        news = []
        for record in UD10Fund.objects.filter(rebalance_date='2018-02-23'):
            news.append(newsfeed.get_news_feed(record.currency.symbol))
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

