import logging
from rest_framework import serializers
from rest_framework.mixins import CreateModelMixin
from oauth2_provider.views.generic import ProtectedResourceView
from datetime import datetime
from DimeAPI.settings.base import REGISTER_STATUS, DASHBOARD_HOSTNAME_URL, \
    EMAIL_ADDRESS_STATUS, USER_STATUS, NAME_TYPE, AUTHORIZATION_CODE_VALID_TIME_IN_SECONDS
from DimeAPI.models import CustomUser, Register, RegisterStatus, Dime10Index, \
    NewsLetter, UserStatus, EmailAddressStatus, EmailAddress, NameType, Name
from DimeAPI.serializer import RegisterSerializer, \
    DimeIndexSerializer, NewsLetterSerializer, CustomUserSerializer
from DimeAPI.classes import ReturnResponse, MyEmail, EmailUtil, UserUtil, UnixEpoch
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


class IndexPage(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class DimeIndex(generics.ListAPIView):
    serializer_class = DimeIndexSerializer
    parser_classes = (JSONParser,)
    queryset = Dime10Index.objects.all()

    def get(self, request, *args, **kwargs):
        pass


class NewsLetterSubscribe(generics.GenericAPIView):
    model = NewsLetter
    permission_classes = (AllowAny, )
    serializer_class = NewsLetterSerializer
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    queryset = NewsLetter.objects.all()

    def post(self, request):
        news_letter = ""
        try:
            news_letter = self.get_serializer(self, data=request.data, partial=True)
            news_letter.is_valid(raise_exception=True)
        except Exception:
            result = 'Failed to parse JSON:{0}'.format(request) + news_letter.errors
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, "failed", result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        if NewsLetter.objects.filter(pk=news_letter.initial_data['email']).exists():
            result = "Email exists."
            logger.error(result)
            return Response(ReturnResponse.Response(1, __name__, "failed", result).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)

        news_letter.create(news_letter.validated_data)
        result = "Joined Mailing List"
        return Response(ReturnResponse.Response(0, __name__, "success", result).return_json(),
                        status=status.HTTP_201_CREATED)


class ReadHistory(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        pass
        # serializer_class = DimeIndexSerializer
        # parser_classes = (JSONParser,)
        # queryset = Dime10Index.objects.all()


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
