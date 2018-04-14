import logging
from DimeAPI.settings.base import DASHBOARD_HOSTNAME_URL
from DimeAPI.models import CustomUser
from DimeAPI.serializer import CustomUserSerializer, GetUserIdSerializer
from DimeAPI.classes import ReturnResponse, MyEmail, UserUtil
from DimeAPI.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.renderers import JSONRenderer
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')


class LoginUser(generics.GenericAPIView):
    permission_classes = (AllowAny, )
    model = CustomUser
    serializer_class = CustomUserSerializer
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        result = '{"redirect_to": "' + DASHBOARD_HOSTNAME_URL + '"}'
        return Response(ReturnResponse.Response(1, __name__, "failed", result).return_json(),
                        status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        result = '{"redirect_to":"' + DASHBOARD_HOSTNAME_URL + '"}'
        logger.error(result)
        return Response(ReturnResponse.Response(1, __name__, "Login Successful", result).return_json(),
                        status=status.HTTP_200_OK)


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
        if user is None:
            return Response(ReturnResponse.Response(1, __name__, 'success', "err").return_json(), status=status.HTTP_400_BAD_REQUEST)
        my_email = MyEmail.MyEmail('Send Forgot Password')
        result = my_email.send_forgot_password_email(user)
        logger.error(result)
        return Response(ReturnResponse.Response(1, __name__, 'success', "Message sent!".format(request.data['email'])).return_json(),
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
        if 'authorizationCode' not in request.data:
            return Response(ReturnResponse.Response(1, __name__, 'failed', "autherizationCode required").return_json(),
                            status=status.HTTP_403_FORBIDDEN)
        if request.data['password'] != request.data['passwordConfirm']:
            return Response(ReturnResponse.Response(1, __name__, 'failed', "passwords do not match").return_json(),
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        my_email = MyEmail.MyEmail('Send Forgot Password')
        result = my_email.send_reset_password_email(request.data)
        return Response(ReturnResponse.Response(1, __name__, 'success', result).return_json(), status=status.HTTP_200_OK)


class LogoutUser(generics.ListAPIView):
    model = CustomUser


class GetUserId(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    model = CustomUser
    serializer_class = GetUserIdSerializer
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    queryset = CustomUser.objects.all()


    def post(self, request):
        if not request.data['Username']:
            return Response(ReturnResponse.Response(1, __name__, 'error', 0).return_json(),
                            status=status.HTTP_400_BAD_REQUEST)
        if len(request.data['Username']) <= 5:
            return Response(ReturnResponse.Response(1, __name__, 'error', 0).return_json(), status=status.HTTP_400_BAD_REQUEST)
        try:
            custom_user = CustomUser.objects.get(email=request.data['Username'])
        except ObjectDoesNotExist as error:
            logger.error(error)
            return Response(ReturnResponse.Response(1, __name__, "error", 0).return_json(),
                status=status.HTTP_400_BAD_REQUEST)
        return Response(ReturnResponse.Response(0, __name__, "success", custom_user.pk).return_json(),
            status=status.HTTP_200_OK)

