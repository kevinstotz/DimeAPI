import logging
import json
from django.core.files.storage import FileSystemStorage
from rest_framework import serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.mixins import CreateModelMixin
from django.apps import apps
from rest_framework import serializers
from rest_framework.mixins import CreateModelMixin
from oauth2_provider.views.generic import ProtectedResourceView
from datetime import datetime, timedelta
from DimeAPI.settings.base import REGISTER_STATUS, DASHBOARD_HOSTNAME_URL, \
    EMAIL_ADDRESS_STATUS, USER_STATUS, NAME_TYPE, AUTHORIZATION_CODE_VALID_TIME_IN_SECONDS, XCHANGE
from DimeAPI.models import CustomUser, Register, RegisterStatus, DimeFund, \
    NewsLetter, UserStatus, EmailAddressStatus, EmailAddress, NameType, Name, DimeHistory, \
    DimePeriod, ContactUsForm, Affiliate, Country, State, City, ZipCode, UserProfile, Document, FileType, DocumentType, DocumentStatus

from DimeAPI.serializer import RegisterSerializer, DimeTableChartSerializer, ContactUsFormSerializer, GetUserIdSerializer, \
    NewsLetterSerializer, CustomUserSerializer, DimeHistorySerializer, DimePieChartSerializer, UserProfileSerializer, \
    DimeRebalanceDateValueSerializer, RegisterAffiliateSerializer, CountrySerializer, DimeTableListChartSerializer, \
    DocumentSerializer, CoinNewsSerializer, DocumentTypeSerializer, DocumentSerializer



from DimeAPI.classes import ReturnResponse, MyEmail, EmailUtil, UserUtil, UnixEpoch, NewsFeed

from django_filters.rest_framework import DjangoFilterBackend

from DimeAPI.permissions import IsAuthenticatedOrCreate, IsAuthenticated
from DimeAPI.classes.UserUtil import get_client_ip
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser
from rest_framework import viewsets, views

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
            contact_us = ContactUsFormSerializer(data=request.data, partial=True)
            contact_us.is_valid(raise_exception=True)
        except Exception:
            result = 'Failed to parse JSON:{0}'.format(request) + contact_us
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
    queryset = DimeHistory.objects.all().filter(xchange=XCHANGE['COIN_MARKET_CAP'])
    filter_backends = (DjangoFilterBackend,)
    ordering = ('name',)
    filter_fields = ('xchange',)



class UserDocuments(generics.ListAPIView):
    model = Document
    serializer_class = DocumentSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = Document.objects.all()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)


class DocumentTypes(generics.ListAPIView):
    model = DocumentType
    serializer_class = DocumentTypeSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = DocumentType.objects.all()



class DimeRebalanceDateValue(generics.ListAPIView):
    model = DimePeriod
    serializer_class = DimeRebalanceDateValueSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = DimePeriod.objects.all()[1:]


class DimePieChart(generics.ListAPIView):
    model = DimeFund
    serializer_class = DimePieChartSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = DimeFund.objects.filter(rebalance_date='2018-02-23')


class CoinNews(generics.ListAPIView):
    model = DimeFund
    serializer_class = CoinNewsSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        newsfeed = NewsFeed.NewsFeed()
        news = []
        for record in DimeFund.objects.filter(rebalance_date='2018-02-23'):
            news.append(newsfeed.get_news_feed(record.currency.symbol))
        return Response(ReturnResponse.Response(0, __name__, json.dumps(news), 0).return_json(),
                            status=status.HTTP_200_OK)


class DimeTableChart(generics.ListAPIView):
    model = DimeFund
    serializer_class = DimeTableChartSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = DimeFund.objects.filter(rebalance_date='2018-02-23')


class DimeTableListChart(generics.ListAPIView):
    model = DimeFund
    serializer_class = DimeTableListChartSerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = DimeFund.objects.filter(rebalance_date='2018-02-23')


class CountryView(generics.ListAPIView):
    model = Country
    serializer_class = CountrySerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = Country.objects.all().order_by('name')


class CityView(generics.ListAPIView):
    model = City
    serializer_class = CountrySerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = City.objects.all().order_by('name')

    def get_queryset(self):
        state = self.kwargs['State']
        return City.objects.filter(state__pk=state)


class StateView(generics.ListAPIView):
    model = State
    serializer_class = CountrySerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = State.objects.all().order_by('name')

    def get_queryset(self):
        country = self.kwargs['Country']
        return State.objects.filter(country__pk=country)


class ZipCodeView(generics.ListAPIView):
    model = ZipCode
    serializer_class = CountrySerializer
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    queryset = ZipCode.objects.all().order_by('zip_code')

    def get_queryset(self):
        city = self.kwargs['City']
        return ZipCode.objects.filter(city__pk=city)


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
            result = 'Failed to parse JSON:{0}:{1}'.format(request, error)
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


class DocumentUpload(views.APIView):
    model = Document
    parser_classes = (FileUploadParser, )
    permission_classes = (AllowAny,)

    def post(self, request, filename, format=None):
        print(request.data['file'])
        file_obj = request.data['file']
        #  print(request.FILES)
        #  myfile = request.data['file']
        #  fs = FileSystemStorage()
        #  filename = fs.save(request.data['file'], myfile)
        document = Document()
        document.document = file_obj
        document.file_type = FileType.objects.get(pk=1)
        document.status = DocumentStatus.objects.get(pk=1)
        document.type = DocumentType.objects.get(pk=1)
        document.save()
        return Response(ReturnResponse.Response(1, __name__, 'success', "u").return_json(),
                        status=status.HTTP_201_CREATED)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as error:
            result = '{0}:'.format(error)
            logger.error(result)
            logger.error(serializer.errors)
            return Response(ReturnResponse.Response(1, __name__, 'Exists', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            result = 'Failed parsing JSon:{0}'.format(request)
            logger.error(result)
            logger.error(error)
            return Response(ReturnResponse.Response(1, __name__, 'Failed parsing Json', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        result = "f"
        logger.debug(result)
        return Response(ReturnResponse.Response(1, __name__, 'success', result).return_json(),
                        status=status.HTTP_201_CREATED)


# LoginRequiredMixin,
class UserProfileView(generics.ListAPIView):
    model = UserProfile
    permission_classes = (AllowAny,)
    serializer_class = UserProfileSerializer
    lookup_url_kwarg = 'User_Id'
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        return UserProfile.objects.filter(customUser__pk=user_id)


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


class RegisterAffiliate(CreateModelMixin, viewsets.GenericViewSet):
    model = Affiliate
    permission_classes = (AllowAny,)
    serializer_class = RegisterAffiliateSerializer
    queryset = Affiliate.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = RegisterAffiliateSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            register_affiliate = serializer.save()
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
            logger.error(register_affiliate.errors)
            return Response(ReturnResponse.Response(1, __name__, 'Failed parsing Json', result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        my_email = MyEmail.MyEmail('Register Affiliate')

        result = my_email.send_register_affiliate_email(register_affiliate)
        logger.debug(result)
        return Response(ReturnResponse.Response(1, __name__, 'success', result).return_json(),
                        status=status.HTTP_201_CREATED)

    def post(self, request):
        print(request.data)


class ForgotPassword(generics.ListAPIView):
    model = CustomUser
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def post(self, request):

        if not request.data['email']:
            return Response(ReturnResponse.Response(1, __name__, 'success', "err").return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        if len(request.data['email']) <= 5:
            return Response(ReturnResponse.Response(1, __name__, 'success', "err").return_json(), status=status.HTTP_400_BAD_REQUEST)
        user = UserUtil.get_user_from_email(request.data['email'])
        if user == None:
            return Response(ReturnResponse.Response(1, __name__, 'success', "err").return_json(), status=status.HTTP_400_BAD_REQUEST)
        my_email = MyEmail.MyEmail('Send Forgot Password')
        result = my_email.send_forgot_password_email(user)
        logger.error(result)
        return Response(ReturnResponse.Response(1, __name__, 'success', "Message sent!".format(request.data['email'])).return_json(),
                        status=status.HTTP_200_OK)


class GetUserId(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    model = CustomUser
    permission_classes = (IsAuthenticated,)
    serializer_class = GetUserIdSerializer
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    queryset = CustomUser.objects.all()

    def post(self, request):
        print(request.data['Username'])
        if not request.data['Username']:
            return Response(ReturnResponse.Response(1, __name__, 'error', 0).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        if len(request.data['Username']) <= 5:
            return Response(ReturnResponse.Response(1, __name__, 'error', 0).return_json(), status=status.HTTP_400_BAD_REQUEST)
        try:
            custom_user = CustomUser.objects.get(email=request.data['Username'])
        except ObjectDoesNotExist as error:
            return Response(ReturnResponse.Response(1, __name__, "error", 0).return_json(),
                    status=status.HTTP_400_BAD_REQUEST)
        return Response(ReturnResponse.Response(0, __name__, "success", custom_user.pk).return_json(),
                    status=status.HTTP_200_OK)


class ResetPassword(generics.ListAPIView):
    model = CustomUser
    permission_classes = (AllowAny,)
    queryset = CustomUser.objects.all()

    def post(self, request):
        if not 'password' in request.data:
            return Response(ReturnResponse.Response(1, __name__, 'failed', "Password required").return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        if not 'passwordConfirm' in request.data:
            return Response(ReturnResponse.Response(1, __name__, 'failed', "Password Confirm required").return_json(),
                            status=status.HTTP_401_UNAUTHORIZED)
        if not 'authorizationCode' in request.data:
            return Response(ReturnResponse.Response(1, __name__, 'failed', "autherizationCode required").return_json(),
                            status=status.HTTP_403_FORBIDDEN)
        if request.data['password'] != request.data['passwordConfirm']:
            return Response(ReturnResponse.Response(1, __name__, 'failed', "passwords do not match").return_json(),
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        my_email = MyEmail.MyEmail('Send Forgot Password')
        result = my_email.send_reset_password_email(request.data)
        return Response(ReturnResponse.Response(1, __name__, 'success', result).return_json(), status=status.HTTP_200_OK)


class LogoutUser(generics.ListAPIView):
    model = Register



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
