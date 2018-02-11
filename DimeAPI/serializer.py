from datetime import datetime
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from DimeAPI.models import Register, RegisterStatus, CustomUser, Dime10Index, NewsLetter, UserAgent, Password
from DimeAPI.settings.base import REGISTER_STATUS, AUTHORIZATION_CODE_LENGTH
from DimeAPI.classes.UserUtil import get_authorization_code
from DimeAPI.classes.EmailUtil import EmailUtil


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email',)


class DimeIndexSerializer(ModelSerializer):

    class Meta:
        model = Dime10Index
        fields = ('id', 'currency',)


class HistorySerializer(ModelSerializer):
    class Meta:
        model = Dime10Index
        fields = ('id', 'currency', 'totalCoinSupply',)


class NewsLetterSerializer(ModelSerializer):
    class Meta:
        model = NewsLetter
        fields = ('email', 'timestamp',)

    def create(self, validated_data):
        return NewsLetter.objects.create(**validated_data)


class RegisterStatusSerializer(ModelSerializer):

    class Meta:
        model = RegisterStatus
        fields = ('id', 'status',)


class PasswordSerializer(ModelSerializer):

    class Meta:
        model = Password
        fields = ('id', 'password',)


class UserAgentSerializer(ModelSerializer):

    class Meta:
        model = UserAgent
        fields = ('userAgent', 'os', 'browser', 'device', 'os_version', 'browser_version',)


class RegisterSerializer(ModelSerializer):
    deviceInfo = UserAgentSerializer()
    status = RegisterStatus()

    class Meta:
        model = Register
        fields = ('email', 'password', 'ipAddress', 'authorizationCode', 'deviceInfo',
                  'status', 'inserted', 'firstName', 'lastName',)
        read_only_fields = ('ipAddress', 'authorizationCode', 'inserted',)
        extra_kwargs = {
            'authorizationCode ': {'required': False},
            'ipAddress ': {'required': False}
        }

    def create(self, validated_data):
        device_info = validated_data.pop('deviceInfo')
        user_agent = UserAgent.objects.create(**device_info)
        return Register.objects.create(**validated_data,
                                       authorizationCode=get_authorization_code(),
                                       inserted=datetime.utcnow(),
                                       status=RegisterStatus.objects.get(pk=REGISTER_STATUS['SENT']),
                                       deviceInfo=user_agent)

    def validate_email(self, value):
        email_util = EmailUtil()
        if email_util.find_email(value) != 0:
            raise serializers.ValidationError("Email Address Already Exists")
        return value

    def validate_authorizationCode(value):
        if len(value) != AUTHORIZATION_CODE_LENGTH:
            raise serializers.ValidationError("Authorization Code Invalid")
        return value

