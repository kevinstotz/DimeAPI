from DimeAPI.settings.base import REGISTER_STATUS, EMAIL_ADDRESS_STATUS, USER_STATUS, NAME_TYPE, \
    AUTHORIZATION_CODE_VALID_TIME_IN_SECONDS, EMAIL_ADDRESS_TYPE

from DimeAPI.models import CustomUser, Register, RegisterStatus, UserStatus, EmailAddressStatus, \
    EmailAddress, NameType, Name, EmailAddressType, Affiliate, UserProfile, Address, ZipCode, City, State, Country
from DimeAPI.serializer import RegisterSerializer, RegisterAffiliateSerializer

from DimeAPI.classes import ReturnResponse, MyEmail, EmailUtil, UserUtil, UnixEpoch

from DimeAPI.permissions import IsAuthenticated
from DimeAPI.classes.UserUtil import get_client_ip
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, status
from rest_framework.mixins import CreateModelMixin
from rest_framework import serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


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
        pass


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


class VerifyRegister(generics.ListAPIView):
    model = Register
    permission_classes = (AllowAny,)
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

        user_profile = UserProfile()
        user_profile.save()
        new_user = CustomUser(email=verify_register.email,
                              username=user_util.new_username,
                              status=UserStatus.objects.get(pk=USER_STATUS['ACTIVE']),
                              user_profile=user_profile)
        try:
            pw = UserUtil.generate_password()
            new_user.set_password(pw)
            new_user.save()
        except Exception as e:
            print(type(e))
            print(e)
            print(e.args)

        email = EmailAddress(email=verify_register.email,
                             user_profile=user_profile,
                             type=EmailAddressType(pk=EMAIL_ADDRESS_TYPE['PRIMARY']),
                             status=EmailAddressStatus(pk=EMAIL_ADDRESS_STATUS['ACTIVE']))

        first_name = Name(name=verify_register.firstName,
                          type=NameType.objects.get(pk=NAME_TYPE['FIRST']),
                          user_profile=user_profile)

        last_name = Name(name=verify_register.lastName,
                         type=NameType.objects.get(pk=NAME_TYPE['LAST']),
                         user_profile=user_profile)
        try:
            for zipcode in ZipCode.objects.filter(zipcode=verify_register.zipCode):
                for state in State.objects.filter(zip_codes=zipcode):
                    s = State.objects.get(pk=state.pk)
                    c = Country.objects.get(pk=state.country.pk)
                    z = ZipCode.objects.get(pk=zipcode.pk)
                    address = Address(country=c,
                                      state=s,
                                      zipcode=z,
                                      user_profile=user_profile)
                    break
                break
        except Exception as error:
            logger.error(error)
            address = Address(user_profile=user_profile)


        address.save()
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
