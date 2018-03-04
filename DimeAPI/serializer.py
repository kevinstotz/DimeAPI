import time
from datetime import datetime
import calendar
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from DimeAPI.models import Register, RegisterStatus, CustomUser, DimeFund, NewsLetter, UserAgent, \
    Password, Currency, DimeHistory, Notification, ContactUsForm, DimePeriod, Xchange, Affiliate
from DimeAPI.settings.base import REGISTER_STATUS, AUTHORIZATION_CODE_LENGTH, XCHANGE
from DimeAPI.classes.UserUtil import get_authorization_code
from DimeAPI.classes.EmailUtil import EmailUtil
from django.core.exceptions import ObjectDoesNotExist

class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email',)


class DimePeriodSerializer(ModelSerializer):

    class Meta:
        model = DimePeriod
        fields = ('start_date', 'end_date',)


class DimeHistorySerializer(ModelSerializer):
    name = serializers.SerializerMethodField('ts_to_date', source='time')
    value = serializers.SerializerMethodField('to_currency')
    rebalance = serializers.SerializerMethodField('is_rebalance_date', source='time')

    class Meta:
        model = DimeHistory
        fields = ('name', 'value', 'rebalance')

    def ts_to_date(self, obj):
        return datetime.utcfromtimestamp(obj.time).strftime('%Y-%m-%d')

    def to_currency(self, obj):
        return '{:.2f}'.format(obj.value * 100.0)

    def is_rebalance_date(self, obj):
        try:
            DimePeriod.objects.get(start_date=datetime.utcfromtimestamp(obj.time).strftime('%Y-%m-%d'))
        except ObjectDoesNotExist as error:
            return 0
        return 1


class CurrencySerializer(ModelSerializer):

    class Meta:
        model = Currency
        fields = ('id', 'name', 'symbol', 'coinName', 'fullName',)


class DimeRebalanceDateValueSerializer(ModelSerializer):
    name = serializers.DateField(source='start_date')
    value = serializers.SerializerMethodField(source='start_date', method_name='to_value')

    class Meta:
        model = DimePeriod
        fields = ('name', 'value',)

    def to_value(self, obj):

        try:
            xchange = Xchange.objects.get(pk=XCHANGE['COIN_MARKET_CAP'])
            dimeHistory = DimeHistory.objects.get(time=int(calendar.timegm(obj.start_date.timetuple())), xchange=xchange)
        except:
            print("could not get entry in history for {0}".format(int(calendar.timegm(obj.start_date.timetuple()))))
            return 0
        return '{:.2f}'.format(dimeHistory.value)


class DimePieChartSerializer(ModelSerializer):
    name = serializers.SlugRelatedField(many=False, read_only=True, source='currency', slug_field='symbol')
    value = serializers.FloatField(source='percent_of_dime')

    class Meta:
        model = DimeFund
        fields = ('name', 'value',)


class DimeTableChartSerializer(ModelSerializer):
    name = serializers.SlugRelatedField(many=False, read_only=True, source='currency', slug_field='symbol')
    value = serializers.FloatField(source='percent_of_dime')

    class Meta:
        model = DimeFund
        fields = ('rank', 'name', 'value', 'percent_of_dime', 'market_cap')


class DimePeriodSerializer(ModelSerializer):

    class Meta:
        model = DimeFund
        fields = ('rebalance_price', 'rank', 'level', 'period', 'currency',
                  'market_cap', 'percent_of_dime', 'amount', 'rebalance_value', 'end_price', 'end_value',)


class NewsLetterSerializer(ModelSerializer):
    timestamp = serializers.SerializerMethodField(method_name='to_utcts')

    class Meta:
        model = NewsLetter
        fields = ('email', 'timestamp',)

    def to_utcts(self, obj):
        return time.mktime(datetime.utcnow().timetuple())


class NotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = ('id',)


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


class ContactUsFormSerializer(ModelSerializer):
    pass

    class Meta:
        model = ContactUsForm
        fields = ('name', 'email', 'message', 'subject',)


class RegisterSerializer(ModelSerializer):
    deviceInfo = UserAgentSerializer()
    status = RegisterStatus()

    class Meta:
        model = Register
        fields = ('email', 'password', 'ipAddress', 'authorizationCode', 'deviceInfo',
                  'status', 'inserted', 'firstName', 'lastName', 'zipCode')
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


class RegisterAffiliateSerializer(ModelSerializer):

    status = RegisterStatus()

    class Meta:
        model = Affiliate
        fields = ('email', 'companyName', 'status', 'inserted', 'firstName', 'lastName', 'zipCode')
        read_only_fields = ('inserted',)

    def create(self, validated_data):
        return Affiliate.objects.create(**validated_data,
                                        inserted=datetime.utcnow(),
                                        status=RegisterStatus.objects.get(pk=REGISTER_STATUS['SENT']))

    def validate_email(self, value):
        email_util = EmailUtil()
        if email_util.find_email(value) != 0:
            raise serializers.ValidationError("Email Address Already Exists")
        return value
