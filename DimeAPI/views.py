import logging
from django.apps import apps
from rest_framework import serializers
from rest_framework.mixins import CreateModelMixin
from oauth2_provider.views.generic import ProtectedResourceView
from datetime import datetime, timedelta
from DimeAPI.settings.base import REGISTER_STATUS, DASHBOARD_HOSTNAME_URL, \
    EMAIL_ADDRESS_STATUS, USER_STATUS, NAME_TYPE, AUTHORIZATION_CODE_VALID_TIME_IN_SECONDS, XCHANGE
from DimeAPI.models import CustomUser, Register, RegisterStatus, DimeMutualFund, \
    NewsLetter, UserStatus, EmailAddressStatus, EmailAddress, NameType, Name, Xchange, Period, DimeHistory, \
    Notification, ContactUsForm
from DimeAPI.serializer import RegisterSerializer, DimeTableChartSerializer, ContactUsFormSerializer, \
    DimeIndexSerializer, NewsLetterSerializer, CustomUserSerializer, DimeHistorySerializer, DimePieChartSerializer, \
    DimeRebalanceDateValueSerializer
from DimeAPI.classes import ReturnResponse, MyEmail, EmailUtil, UserUtil, UnixEpoch
from django_filters.rest_framework import DjangoFilterBackend

from DimeAPI.permissions import IsAuthenticatedOrCreate
from DimeAPI.classes.UserUtil import get_client_ip
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
import calendar

logger = logging.getLogger(__name__)


class LoginUser(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    model = CustomUser
    serializer_class = CustomUserSerializer
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        print('Cannot do a get')
        result = '{"redirect_to": "' + DASHBOARD_HOSTNAME_URL + '"}'
        return Response(ReturnResponse.Response(1, __name__, "failed", result).return_json(),
                        status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        print('logged in')
        result = '{"redirect_to":"' + DASHBOARD_HOSTNAME_URL + '"}'
        logger.error(result)
        return Response(ReturnResponse.Response(1, __name__, "Login Successful", result).return_json(),
                        status=status.HTTP_200_OK)


class ContactUs(generics.CreateAPIView):
    queryset = ContactUsForm.objects.all()
    serializer_class = ContactUsFormSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        contact_us = ''
        try:
            print(request.data)
            contact_us = self.get_serializer(self, data=request.data, partial=True)
            contact_us.is_valid(raise_exception=True)
        except Exception:
            result = 'Failed to parse JSON:{0}'.format(request) + contact_us.errors
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, "Contact Us send Failed", result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        contact_us.create(contact_us.validated_data)
        my_email = MyEmail.MyEmail(name=contact_us.validated_data['name'])
        my_email.send_contact_us(contact_us)
        result = "Email Sent"
        return Response(ReturnResponse.Response(0, __name__, "Email Sent!", result).return_json(),
                        status=status.HTTP_201_CREATED)


class IndexPage(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class DimeLineChart(generics.ListAPIView):
    model = DimeHistory
    serializer_class = DimeHistorySerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = DimeHistory.objects.all()
    filter_backends = (DjangoFilterBackend,)
    ordering = ('name',)
    filter_fields = ('xchange',)


class DimeRebalanceDateValue(generics.ListAPIView):
    model = Period
    serializer_class = DimeRebalanceDateValueSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    now = datetime.utcnow()
    queryset = Period.objects.all()
    queryset = Period.objects.filter(pk__gt=0, pk__lte=5)


class DimePieChart(generics.ListAPIView):
    model = DimeMutualFund
    serializer_class = DimePieChartSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = DimeMutualFund.objects.filter(rebalance_date='2017-12-23')


class DimeTableChart(generics.ListAPIView):
    model = DimeMutualFund
    serializer_class = DimeTableChartSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = DimeMutualFund.objects.filter(rebalance_date='2017-12-23')


class DimeIndex(generics.ListAPIView):
    model = DimeMutualFund
    serializer_class = DimeIndexSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = DimeMutualFund.objects.all()

    def get(self, request, *args, **kwargs):


        values = dict()
        periods = Period.objects.all()[1:]
        for period in periods:
            start_date = datetime.strptime(str(period.start_year) + '-' + str(period.start_month) + '-' + str(period.start_day), '%Y-%m-%d').date()
            rebalance_date = start_date

            end_date = datetime.strptime(str(period.end_year) + '-' + str(period.end_month) + '-' + str(period.end_day), '%Y-%m-%d').date()
            if end_date > datetime.utcnow().date():
                end_date = datetime.utcnow().date()
            while start_date < end_date:

                dimeindex = DimeMutualFund.objects.filter(rebalance_date=rebalance_date)
                running_total = 0
                for coin in dimeindex:
                    coin_class = apps.get_model(app_label='DimeCoins', model_name=coin.currency.symbol)
                    try:
                        xchange_model = apps.get_model('DimeCoins', 'Xchange')
                        xchange_mod = xchange_model.objects.using('coins').get(pk=XCHANGE['COIN_MARKET_CAP'])
                        index = coin_class.objects.using('coins').get(time=int(calendar.timegm(start_date.timetuple())), xchange=xchange_mod)
                    except ObjectDoesNotExist as error:
                        print(error)
                        return
                    except TypeError as error:
                        print(error)
                        return

                    running_total = running_total + coin.amount * index.close
                xchange = Xchange.objects.get(pk=XCHANGE['COIN_MARKET_CAP'])
                dimeHistory = DimeHistory(time=int(calendar.timegm(start_date.timetuple())),
                                          value=running_total,
                                          xchange=xchange)
                dimeHistory.save()
                start_date = start_date + timedelta(days=1)
        return Response(ReturnResponse.Response(1, __name__, "Done", 0).return_json(), status=status.HTTP_200_OK)


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
            print(result)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, "Subscription Failed", result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            news_letter = NewsLetterSerializer(data=request.data, many=False, partial=True)
            news_letter.is_valid(raise_exception=True)
            news_letter.save()
        except Exception as error:
            result = 'Failed to parse JSON:{0}'.format(request) + error
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, "Subscription Failed", result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        result = "Joined Mailing List"
        return Response(ReturnResponse.Response(0, __name__, "Subscription Successful", result).return_json(),
                        status=status.HTTP_201_CREATED)


class ReadHistory(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        pass
        # serializer_class = DimeIndexSerializer
        # parser_classes = (JSONParser,)
        # queryset = DimeMutualFund.objects.all()


class UserInfo(LoginRequiredMixin, generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        login_url = '/login/'
        print('user info')
        redirect_field_name = 'redirect_to'


class RegisterUser(CreateModelMixin, viewsets.GenericViewSet):
    model = Register
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    queryset = Register.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            register_user = serializer.save(ipAddress=get_client_ip(request))
        except serializers.ValidationError as error:
            result = '{0}:'.format(error)
            logger.error(result)
            logger.error(serializer.errors)
            return Response(ReturnResponse.Response(1, __name__, 'Email Address Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            result = 'Failed parsing JSon:{0}'.format(request)
            logger.error(result)
            logger.error(error)
            logger.error(register_user.errors)
            return Response(ReturnResponse.Response(1, __name__, 'Failed parsing Json', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        my_email = MyEmail.MyEmail('Verify Email')

        result = my_email.send_verify_email(register_user)
        logger.debug(result)
        return Response(ReturnResponse.Response(1, __name__, 'success', result).return_json(),
                        status=status.HTTP_201_CREATED)

    def post(self, request):
        print(request.data)


class VerifyRegister(generics.ListAPIView):
    model = Register
    permission_classes = (IsAuthenticatedOrCreate,)
    serializer_class = RegisterSerializer
    queryset = Register.objects.all()
    parser_classes = (JSONParser,)

    def get(self, request, *args, **kwargs):

        authorization_code = kwargs.get('Authorization_Code', 0)

        try:
            self.get_queryset().filter(authorizationCode=authorization_code).count()
            verify_register = Register.objects.get(authorizationCode=authorization_code)
        except ObjectDoesNotExist:
            register_status = RegisterStatus.objects.get(pk=REGISTER_STATUS['INVALID'])
            result = 'Invalid Register Code:{0} :{1}'.format(register_status.status, authorization_code)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'Invalid Register Code', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        if verify_register.status.pk == REGISTER_STATUS['EXPIRED']:
            result = 'Expired Register Code:{0} :{1}'.format(verify_register.status, authorization_code)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'Register Code Expired', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        if verify_register.status.pk == REGISTER_STATUS['VERIFIED']:
            result = 'Already Verified Register Code:{0} :{1}'.format(verify_register.status, authorization_code)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'Register Code already Verified', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        if verify_register.status.pk == REGISTER_STATUS['NEW']:
            result = 'New Register Code:{0} :{1}'.format(verify_register.status, authorization_code)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'Register Code is New', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        if verify_register.status.pk != REGISTER_STATUS['SENT']:
            result = 'Register Code Already Sent:{0} :{1}'.format(verify_register.status, authorization_code)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'Register Code is Sent', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        if (UnixEpoch.datetime_to_epoch(datetime.now()) - UnixEpoch.datetime_to_epoch(verify_register.inserted)) > AUTHORIZATION_CODE_VALID_TIME_IN_SECONDS:
                register_status = RegisterStatus.objects.get(pk=REGISTER_STATUS['EXPIRED'])
                verify_register.status = register_status
                verify_register.save()
                result = 'Register Code Expired:{0} :{1}'.format(verify_register.status, authorization_code)
                logger.error(result)
                return Response(ReturnResponse.Response(1, __name__, 'Register Code Expired', result).return_json(),
                                status=status.HTTP_400_BAD_REQUEST)

        new_user = CustomUser(status=UserStatus.objects.get(pk=USER_STATUS['ACTIVE']))
        user_util = UserUtil.UserUtils()
        if user_util.find_username(verify_register.firstName + verify_register.lastName) != 0:
            result = 'Failed creating username: already exists'
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'Username Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        email_util = EmailUtil.EmailUtil()
        if email_util.find_email(verify_register.email) != 0:
            email_status = EmailAddressStatus.objects.get(pk=EMAIL_ADDRESS_STATUS['EXISTS'])
            result = 'Email Already exists:{0}: {1}:'.format(email_status.status, verify_register.email)
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, 'Email Already Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        new_user.email = verify_register.email
        new_user.username = user_util.new_username
        pw = UserUtil.generate_password()
        new_user.set_password(pw)
        new_user.save()

        email = EmailAddress(email=verify_register.email,
                             user=new_user,
                             status=EmailAddressStatus(pk=EMAIL_ADDRESS_STATUS['ACTIVE']))

        first_name = Name(name=verify_register.firstName,
                          type=NameType.objects.get(pk=NAME_TYPE['FIRST']),
                          user=new_user)

        last_name = Name(name=verify_register.lastName,
                         type=NameType.objects.get(pk=NAME_TYPE['LAST']),
                         user=new_user)

        email.save()
        first_name.save()
        last_name.save()

        my_mail = MyEmail.MyEmail("Welcome Email")
        my_mail.send_welcome_email(new_user, pw)

        verify_register.status = RegisterStatus.objects.get(pk=REGISTER_STATUS['VERIFIED'])
        verify_register.save()

        result = 'User Added:{0}:'.format(new_user.pk)
        logger.info(result)
        return Response(ReturnResponse.Response(1, __name__, 'Registration Succuess!  Welcome Email Sent.', result).return_json(),
                        status=status.HTTP_200_OK)
