import time
import logging
from datetime import datetime
import calendar
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from DimeAPI.models import Register, RegisterStatus, CustomUser, Fund, NewsLetter, UserAgent, State, \
     FundHistory, Notification, ContactUsForm, FundRebalanceDate, Xchange, Affiliate, Name, NameType, City, \
     Document, DocumentType, DocumentStatus, FileType, DepositTransaction, PaypalTransactionResourceAmount, \
     PaypalTransaction, BraintreePaypalTransactionDetails, BraintreePaypalTransaction, BraintreeVisaMCTransactionDetails, \
     UserProfile, Address, ZipCode, PaypalTransactionResource, BraintreeVisaMCTransaction, PhoneNumberType, Country, \
     PhoneNumber, EmailAddressType, EmailAddress, DepositTransactionType, DepositTransactionStatus, WithdrawTransaction, \
     WithdrawTransactionStatus, WithdrawTransactionType, FundCurrency, Currency, FundPeriod
from DimeAPI.settings.base import REGISTER_STATUS, AUTHORIZATION_CODE_LENGTH, XCHANGE, ENGINE_HOSTNAME_NO_PORT, MEDIA_URL, \
    DEPOSIT_TYPE, PAYMENT_GATEWAYS, WITHDRAW_TYPE, DASHBOARD_HOSTNAME_URL
from DimeAPI.classes.UserUtil import get_authorization_code
from DimeAPI.classes.EmailUtil import EmailUtil
from django.core.exceptions import ObjectDoesNotExist


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s (%(threadName)-2s) %(message)s')


class DepositTransactionTypeSerializer(ModelSerializer):

    class Meta:
        model = DepositTransactionType
        read_only_fields = ('id',)
        fields = ('id', 'type',)


class DepositTransactionStatusSerializer(ModelSerializer):

    class Meta:
        model = DepositTransactionStatus
        fields = ('id', 'status',)


class DepositTransactionSerializer(ModelSerializer):
    transactionMethod = serializers.SerializerMethodField(source='deposit_type')
    amount = serializers.SerializerMethodField(source='deposit_id')
    deposit_withdraw = serializers.SerializerMethodField(source='deposit_status')
    status = serializers.SerializerMethodField(source='deposit_status')

    class Meta:
        model = DepositTransaction
        read_only_fields = ('id',)
        fields = ('id', 'inserted', 'status', 'deposit_withdraw', 'amount', 'transactionMethod',)

    def get_deposit_withdraw(self, obj):
        return "Deposit"

    def get_status(self, obj):
        try:
            instance = DepositTransactionStatus.objects.get(pk=obj.deposit_status.pk)
        except ObjectDoesNotExist as error:
            logger.error("{0}".format(error))
            return 0
        return instance.status

    def get_transactionMethod(self, obj):
        try:
            instance = DepositTransactionType.objects.get(pk=obj.deposit_type.pk)
        except ObjectDoesNotExist as error:
            logger.error("{0}".format(error))
            return 0
        return instance.type

    def get_amount(self, obj):
        if DEPOSIT_TYPE['PAYPAL'] == obj.deposit_type.pk:
            if PAYMENT_GATEWAYS['BRAINTREE'] == obj.payment_gateway.pk:
                try:
                    trans = BraintreePaypalTransaction.objects.get(pk=obj.deposit_id, user_profile=self.context['request'].user.user_profile)
                except ObjectDoesNotExist as error:
                    logger.error("{0}".format(error))
                    return 0
                return trans.amount

        if DEPOSIT_TYPE['VISA'] == obj.deposit_type.pk:
            if PAYMENT_GATEWAYS['BRAINTREE'] == obj.payment_gateway.pk:
                try:
                    trans = BraintreeVisaMCTransaction.objects.get(pk=obj.deposit_id, user_profile=self.context['request'].user.user_profile)
                except ObjectDoesNotExist as error:
                    logger.error("{0}".format(error))
                    return 0
                return trans.amount
        return 0


class WithdrawTransactionTypeSerializer(ModelSerializer):

    class Meta:
        model = WithdrawTransactionType
        read_only_fields = ('id',)
        fields = ('id', 'type',)


class WithdrawTransactionStatusSerializer(ModelSerializer):

    class Meta:
        model = WithdrawTransactionStatus
        fields = ('id', 'status',)


class WithdrawTransactionSerializer(ModelSerializer):
    transactionMethod = serializers.SerializerMethodField(source='withdraw_type')
    amount = serializers.SerializerMethodField(source='withdraw_id')
    deposit_withdraw = serializers.SerializerMethodField(source='withdraw_status')
    status = serializers.SerializerMethodField(source='withdraw_status')

    class Meta:
        model = WithdrawTransaction
        read_only_fields = ('id',)
        fields = ('id', 'inserted', 'status', 'deposit_withdraw', 'amount', 'transactionMethod',)

    def get_deposit_withdraw(self, obj):
        return "Withdraw"

    def get_status(self, obj):
        try:
            instance = WithdrawTransactionStatus.objects.get(pk=obj.withdraw_status.pk)
        except ObjectDoesNotExist as error:
            logger.error("{0}".format(error))
            return 0
        return instance.status

    def get_transactionMethod(self, obj):
        try:
            instance = WithdrawTransactionType.objects.get(pk=obj.withdraw_type.pk)
        except ObjectDoesNotExist as error:
            logger.error("{0}".format(error))
            return 0
        return instance.type

    def get_amount(self, obj):
        if WITHDRAW_TYPE['PAYPAL'] == obj.withdraw_type.pk:
            if PAYMENT_GATEWAYS['BRAINTREE'] == obj.withdraw_gateway.pk:
                try:
                    trans = BraintreePaypalTransaction.objects.get(pk=obj.withdraw_id, user_profile=self.context[
                        'request'].user.user_profile)
                except ObjectDoesNotExist as error:
                    logger.error("{0}".format(error))
                    return 0
                return trans.amount

        if WITHDRAW_TYPE['VISA'] == obj.withdraw_type.pk:
            if PAYMENT_GATEWAYS['BRAINTREE'] == obj.payment_gateway.pk:
                try:
                    trans = BraintreeVisaMCTransaction.objects.get(pk=obj.withdraw_id, user_profile=self.context[
                        'request'].user.user_profile)
                except ObjectDoesNotExist as error:
                    logger.error("{0}".format(error))
                    return 0
                return trans.amount
        return 0


class EmailAddressTypeSerializer(ModelSerializer):

    class Meta:
        model = EmailAddressType
        read_only_fields = ('type',)
        fields = ('type',)


class EmailAddressSerializer(ModelSerializer):
    type = EmailAddressTypeSerializer(many=False, read_only=True)

    class Meta:
        model = EmailAddress
        fields = ('email', 'type',)


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = ('name', 'id',)


class DocumentTypeSerializer(ModelSerializer):

    class Meta:
        model = DocumentType
        fields = ('id', 'type',)


class DocumentFileTypeSerializer(ModelSerializer):

    class Meta:
        model = FileType
        fields = ('id', 'type',)


class DocumentStatusSerializer(ModelSerializer):

    class Meta:
        model = DocumentStatus
        fields = ('id', 'status',)


class DocumentSerializer(ModelSerializer):
    file_type = DocumentFileTypeSerializer(many=False, read_only=True)
    type = DocumentTypeSerializer(many=False, read_only=True)
    status = DocumentStatusSerializer(many=False, read_only=True)
    document = serializers.SerializerMethodField('prepend_host', source='document')

    class Meta:
        model = Document
        read_only_fields = ('status', 'type',)
        fields = ('id', 'status', 'name', 'document', 'inserted', 'type', 'size', 'file_type',)

    def prepend_host(self, obj):
        return '{0}{1}{2}'.format(ENGINE_HOSTNAME_NO_PORT, MEDIA_URL, obj.document)


class NameTypeSerializer(ModelSerializer):

    class Meta:
        model = NameType
        fields = ('id', 'type',)


class ZipCodeSerializer(ModelSerializer):

    class Meta:
        model = ZipCode
        fields = ('zipcode', 'id',)


class StateSerializer(ModelSerializer):

    class Meta:
        model = State
        fields = ('name', 'code', 'id',)


class PhoneNumberTypeSerializer(ModelSerializer):

    class Meta:
        model = PhoneNumberType
        fields = ('id', 'type',)


class CountrySerializer(ModelSerializer):

    class Meta:
        model = Country
        fields = ('sort_name', 'name', 'id', 'phone_code')


class PhoneNumberSerializer(ModelSerializer):
    type = PhoneNumberTypeSerializer(many=False, read_only=True)
    country = CountrySerializer(many=False, read_only=True)

    class Meta:
        model = PhoneNumber
        read_only_fields = ('country',)
        fields = ('id', 'phone_number', 'type', 'country', )


class AddressSerializer(ModelSerializer):
    city = CitySerializer(many=False, read_only=True)
    state = StateSerializer(many=False, read_only=True)
    country = CountrySerializer(many=False, read_only=True)
    zipcode = ZipCodeSerializer(many=False, read_only=True)

    class Meta:
        model = Address
        read_only_fields = ('type',)
        fields = ('address1', 'address2', 'address3', 'unit', 'state', 'city', 'country', 'zipcode',)
        depth = 1


class NameSerializer(ModelSerializer):
    type = NameTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Name
        read_only_fields = ('type',)
        fields = ('name', 'type',)


class GetUserIdSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        read_only_fields = ('id',)
        fields = ('id',)


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        read_only_fields = ('id', 'email',)
        fields = ('id', 'email',)


class PaypalTransactionResourceAmountSerializer(ModelSerializer):

    class Meta:
        model = PaypalTransactionResourceAmount
        fields = ('total', 'currency',)


class PaypalTransactionResourceSerializer(ModelSerializer):
    amount = PaypalTransactionResourceAmountSerializer(many=False)

    class Meta:
        model = PaypalTransactionResource
        fields = ('parent_payment', 'update_time', 'create_time', 'amount', 'id', 'state',)


class PaypalTransactionSerializer(ModelSerializer):
    resource = PaypalTransactionResourceSerializer(many=False)

    class Meta:
        model = PaypalTransaction
        fields = ('id', 'create_time', 'resource_type', 'event_type', 'summary', 'resource',)

    def create(self, validated_data):
        resource_data = validated_data.pop('resource')
        amount_data = resource_data.pop('amount')
        paypal_transaction_resource_amount = PaypalTransactionResourceAmount.objects.create(**amount_data)
        paypal_transaction_resource = PaypalTransactionResource.objects.create(amount=paypal_transaction_resource_amount, **resource_data)
        return PaypalTransaction.objects.create(resource=paypal_transaction_resource, **validated_data)


class BraintreePaypalTransactionDetailsSerializer(ModelSerializer):

    class Meta:
        model = BraintreePaypalTransactionDetails
        fields = ('email', 'firstName', 'lastName', 'payerId', 'countryCode',)


class BraintreePaypalTransactionSerializer(ModelSerializer):
    details = BraintreePaypalTransactionDetailsSerializer(many=False)

    class Meta:
        model = BraintreePaypalTransaction
        fields = ('id', 'nonce', 'details', 'type', 'amount',)

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        braintree_paypal_transaction_details = BraintreePaypalTransactionDetails.objects.create(**details_data)
        return BraintreePaypalTransaction.objects.create(details=braintree_paypal_transaction_details, **validated_data)


class BraintreeVisaMCTransactionDetailsSerializer(ModelSerializer):

    class Meta:
        model = BraintreeVisaMCTransactionDetails
        fields = ('cardType', 'lastFour', 'lastTwo',)


class BraintreeVisaMCTransactionSerializer(ModelSerializer):
    details = BraintreeVisaMCTransactionDetailsSerializer(many=False)

    class Meta:
        model = BraintreeVisaMCTransaction
        fields = ('id', 'nonce', 'details', 'type', 'amount',)

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        braintree_visaMC_transaction_details = BraintreeVisaMCTransactionDetails.objects.create(**details_data)
        return BraintreeVisaMCTransaction.objects.create(details=braintree_visaMC_transaction_details, **validated_data)


class UserProfileSerializer(ModelSerializer):
    names = NameSerializer(many=True, read_only=True)
    emailAddresses = EmailAddressSerializer(many=True, read_only=True)
    addresses = AddressSerializer(many=True, read_only=True)
    phoneNumbers = PhoneNumberSerializer(many=True, read_only=True)
    customUser = CustomUserSerializer(many=False, read_only=True)
    avatar = serializers.SerializerMethodField(source='avatar')

    class Meta:
        model = UserProfile
        read_only_fields = ('names', 'emailAddresses', 'addresses', 'phoneNumbers', 'customUser',)
        fields = ('names', 'emailAddresses', 'addresses', 'phoneNumbers', 'customUser', 'avatar', 'about', 'birth_date')

    def get_avatar(self, obj):
        return DASHBOARD_HOSTNAME_URL + "/assets/images/profiles/" + str(self.context[
                        'request'].user.user_profile.pk) + "/" + str(obj.avatar)


class FundHistorySerializer(ModelSerializer):
    name = serializers.SerializerMethodField('ts_to_date', source='time')
    value = serializers.SerializerMethodField('to_currency')
    rebalance = serializers.SerializerMethodField('is_rebalance_date', source='time')

    class Meta:
        model = FundHistory
        fields = ('name', 'value', 'rebalance')

    def ts_to_date(self, obj):
        return datetime.utcfromtimestamp(obj.time).strftime('%Y-%m-%d')

    def to_currency(self, obj):
        return '{:.2f}'.format(obj.value * 100.0)

    def is_rebalance_date(self, obj):
        try:
            FundRebalanceDate.objects.get(start_date=datetime.utcfromtimestamp(obj.time).strftime('%Y-%m-%d'))
        except ObjectDoesNotExist as error:
            logger.error("{0}".format(error))
            return 0
        return 1


class FundPeriodSerializer(ModelSerializer):

    class Meta:
        model = FundPeriod
        fields = ('id', 'period',)


class FundRebalanceDateValueSerializer(ModelSerializer):
    name = serializers.DateField(source='start_date')
    value = serializers.SerializerMethodField(source='start_date', method_name='to_value')

    class Meta:
        model = FundRebalanceDate
        fields = ('name', 'value',)

    def to_value(self, obj):

        try:
            xchange = Xchange.objects.get(pk=XCHANGE['COIN_MARKET_CAP'])
            fundHistory = FundHistory.objects.get(time=int(calendar.timegm(obj.start_date.timetuple())), xchange=xchange)
        except Exception as error:
            logger.error("Could not get entry in history for {0}: {1}".format(int(calendar.timegm(obj.start_date.timetuple())), error))
            return 0
        return '{:.2f}'.format(fundHistory.value)


class FundPieChartSerializer(ModelSerializer):
    name = serializers.SerializerMethodField(source='currency')
    value = serializers.FloatField(source='percent')

    class Meta:
        model = FundCurrency
        fields = ('name', 'value',)

    def get_name(self, obj):
        try:
            currency = Currency.objects.using('coins').get(id=obj.currency)
        except ObjectDoesNotExist as error:
            logger.error("{0}".format(error))
            return
        except Exception as error:
            logger.error("{0}".format(error))
            return
        return currency.symbol


class FundLineChartSerializer(ModelSerializer):
    name = serializers.SerializerMethodField(source='time')
    rebalance = serializers.SerializerMethodField(source='time')

    class Meta:
        model = FundHistory
        fields = ('name', 'value', 'rebalance')

    def get_name(self, obj):
        return obj.time

    def get_rebalance(self, obj):
        try:
            FundRebalanceDate.objects.get(start_date=obj.time, fund=obj.fund)
            return 1
        except ObjectDoesNotExist as error:
            logger.error("{0}".format(error))
            return 0
        return 0


class FundTableChartSerializer(ModelSerializer):
    name = serializers.SerializerMethodField(source='currency')
    value = serializers.FloatField(source='percent')

    class Meta:
        model = FundCurrency
        fields = ('rank', 'name', 'value', 'percent', 'market_cap', 'end_price',)

    def get_name(self, obj):
        try:
            currency = Currency.objects.using('coins').get(id=obj.currency)
        except ObjectDoesNotExist as error:
            logger.error("{0}".format(error))
            return
        except Exception as error:
            logger.error("{0}".format(error))
            return
        return currency.symbol


class FundTableListChartSerializer(ModelSerializer):
    name = serializers.SerializerMethodField(source='currency')

    class Meta:
        model = FundCurrency
        read_only_fields = ('symbol',)
        fields = ('rank', 'percent', 'rebalance_price', 'end_price', 'name')

    def get_name(self, obj):
        try:
            currency = Currency.objects.using('coins').get(id=obj.currency)
        except ObjectDoesNotExist as error:
            logger.error("{0}".format(error))
            return
        except Exception as error:
            logger.error("{0}".format(error))
            return
        return currency.symbol


class FundRebalanceDateSerializer(ModelSerializer):

    class Meta:
        model = FundRebalanceDate
        fields = ('rebalance_price', 'rank', 'level', 'rebalance_date', 'currency',
                  'market_cap', 'percent', 'amount', 'rebalance_value', 'end_price', 'end_value',)


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


class UserAgentSerializer(ModelSerializer):

    class Meta:
        model = UserAgent
        fields = ('userAgent', 'codeName', 'appName', 'appVersion', 'cookiesEnabled', 'language', 'platform',)


class ContactUsFormSerializer(ModelSerializer):

    class Meta:
        model = ContactUsForm
        fields = ('name', 'email', 'message', 'subject',)


class RegisterSerializer(ModelSerializer):
    userAgent = UserAgentSerializer()
    status = RegisterStatus()

    class Meta:
        model = Register
        fields = ('email', 'password', 'ipAddress', 'authorizationCode', 'userAgent',
                  'status', 'inserted', 'firstName', 'lastName', 'zipCode')
        read_only_fields = ('ipAddress', 'authorizationCode', 'inserted',)
        extra_kwargs = {
            'authorizationCode ': {'required': False},
            'ipAddress ': {'required': False}
        }

    def create(self, validated_data):
        userAgent = validated_data.pop('userAgent')
        user_agent = UserAgent.objects.create(**userAgent)
        return Register.objects.create(**validated_data,
                                       authorizationCode=get_authorization_code(),
                                       inserted=datetime.utcnow(),
                                       status=RegisterStatus.objects.get(pk=REGISTER_STATUS['SENT']),
                                       userAgent=user_agent)

    def validate_email(self, value):
        email_util = EmailUtil()
        if email_util.find_email(value) != 0:
            raise serializers.ValidationError("Email Address Already Exists")
        return value

    def validate_authorizationCode(self, value):
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
