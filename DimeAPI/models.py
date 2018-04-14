from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from DimeAPI.settings.base import EMAIL_LENGTH, ADDRESS_LENGTH, FIRST_NAME_LENGTH, \
    LAST_NAME_LENGTH, AUTHORIZATION_CODE_LENGTH, EMAIL_TEMPLATE_DIR, \
    COIN_SYMBOL_LENGTH, COIN_NAME_LENGTH, COIN_FULL_NAME_LENGTH, PASSWORD_LENGTH, AUTH_USER_MODEL, NONCE_LENGTH
from .managers import UserManager


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=COIN_NAME_LENGTH, default="dd", blank=False)
    symbol = models.CharField(max_length=COIN_SYMBOL_LENGTH, default="dd", blank=False)
    coin_name = models.CharField(max_length=COIN_NAME_LENGTH, default="dd")
    full_name = models.CharField(max_length=COIN_FULL_NAME_LENGTH, default="dd")
    class_name = models.CharField(max_length=50, default="dd", blank=False)
    coinmarketcap = models.CharField(max_length=100, default="dd", blank=True)
    active = models.BooleanField(default=False, verbose_name="Active Currency")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        db_table = 'DimeCoins_currency'
        managed = False
        ordering = ('id',)


class UserProfile(models.Model):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.pk

    class Meta:
        ordering = ('id',)


class PaymentGateway(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="NA", blank=False)
    username = models.CharField(max_length=100, default="NA", blank=False)
    password = models.CharField(max_length=100, default="NA", blank=False)
    transaction_flat_fee = models.FloatField(default=0.0, blank=False)
    transaction_percentage_fee = models.FloatField(default=0.0, blank=False)
    public_key = models.CharField(max_length=255, default="NA", blank=False)
    client_id = models.CharField(max_length=255, default="NA", blank=False)
    client_secret = models.CharField(max_length=255, default="NA", blank=False)
    private_key = models.CharField(max_length=255, default="NA", blank=False)
    token_key = models.CharField(max_length=255, default="NA", blank=False)
    encryption_key = models.TextField(default="NA", blank=False)
    merchant_id = models.CharField(max_length=255, default="NA", blank=False)
    environment = models.CharField(max_length=100, default="NA", blank=False)
    api_url = models.CharField(max_length=255, default="NA", blank=False)
    api_key = models.CharField(max_length=255, default="NA", blank=False)
    active = models.BooleanField(default=False, verbose_name="Active Payment Gateway")

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('name',)


class PaypalTransactionResourceAmount(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.FloatField(default=0.0, blank=False)
    currency = models.CharField(max_length=10, default="NA", blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.total

    class Meta:
        ordering = ('total',)


class PaypalTransactionResource(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default="NA", blank=False)
    parent_payment = models.CharField(max_length=100, default="NA", blank=False)
    update_time = models.DateTimeField()
    create_time = models.DateTimeField()
    amount = models.ForeignKey(PaypalTransactionResourceAmount,
                               on_delete=models.PROTECT,
                               verbose_name="Paypal Transaction Resource Amount",
                               default=1,
                               related_name='paypalTransactionResourceAmount')
    state = models.CharField(max_length=30, default="NA", blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class PaypalTransaction(models.Model):
    id = models.CharField(primary_key=True, max_length=100, default="NA", blank=False)
    create_time = models.DateTimeField()
    resource_type = models.CharField(max_length=50, default="NA", blank=False)
    event_type = models.CharField(max_length=100, default="NA", blank=False)
    summary = models.CharField(max_length=255, default="NA", blank=False)
    resource = models.ForeignKey(PaypalTransactionResource,
                                 on_delete=models.PROTECT,
                                 verbose_name="Paypal Transaction Resource",
                                 default=1,
                                 related_name='paypalTransactionResource')
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class BraintreePaypalTransactionDetails(models.Model):
    id = models.AutoField(primary_key=True)
    shippingAddress = models.CharField(max_length=40, default="NA", blank=True)
    email = models.CharField(max_length=EMAIL_LENGTH, default="NA", blank=False)
    firstName = models.CharField(max_length=FIRST_NAME_LENGTH, default="NA", blank=True)
    lastName = models.CharField(max_length=FIRST_NAME_LENGTH, default="NA", blank=True)
    payerId = models.CharField(max_length=20, default="NA", blank=False)
    countryCode = models.CharField(max_length=6, default="NA", blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class BraintreePaypalTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.PROTECT,
                                     verbose_name='Userprofile of Paypal Transaction',
                                     default=1,
                                     related_name='userProfilePaypalTransaction')
    nonce = models.CharField(max_length=NONCE_LENGTH, default="NA", blank=False)
    amount = models.FloatField(default=0.0, blank=True)
    type = models.CharField(max_length=40, default="NA", blank=False)
    details = models.ForeignKey(BraintreePaypalTransactionDetails,
                                on_delete=models.PROTECT,
                                verbose_name='Braintree Paypal Transaction Details',
                                default=1,
                                related_name='braintreePaypalTransactionDetails')
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class BraintreeVisaMCTransactionDetails(models.Model):
    id = models.AutoField(primary_key=True)
    cardType = models.CharField(max_length=40, default="NA", blank=True)
    lastFour = models.IntegerField(blank=True, default=0)
    lastTwo = models.IntegerField(blank=True, default=0)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class BraintreeVisaMCTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.PROTECT,
                                     verbose_name='Userprofile of VisaMC Transaction',
                                     default=1,
                                     related_name='userProfileVisaMcTransaction')
    nonce = models.CharField(max_length=NONCE_LENGTH, default="NA", blank=False)
    amount = models.FloatField(default=0.0, blank=True)
    type = models.CharField(max_length=30, default="NA", blank=False)
    details = models.ForeignKey(BraintreeVisaMCTransactionDetails,
                                on_delete=models.PROTECT,
                                verbose_name='Braintree VisaMC Transaction Details',
                                default=1,
                                related_name='braintreeVisaMCTransactionDetails')
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class HouseFund(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="NA", blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('name',)


class HouseFee(models.Model):
    id = models.AutoField(primary_key=True)
    fund = models.ForeignKey(HouseFund,
                             on_delete=models.PROTECT,
                             verbose_name='House Fund',
                             default=1,
                             related_name='houseFund')
    yearly_fee = models.FloatField(default=0.0)
    yearly_fee_start_date = models.DateTimeField(verbose_name="Date when Yearly Fee Started")
    performance_fee = models.FloatField(default=0.0)
    performance_fee_start_date = models.DateTimeField(verbose_name="Date when Performance Fee Started")
    period_fee = models.FloatField(default=0.0)
    period_fee_start_date = models.DateTimeField(verbose_name="Date when Yearly Fee Started")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class DepositTransactionStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=40, verbose_name="Status of Deposit Transaction")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.status

    class Meta:
        ordering = ('id',)


class WithdrawTransactionStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=40, verbose_name="Status of Withdraw Transaction")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.status

    class Meta:
        ordering = ('id',)


class DepositTransactionType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=40, verbose_name="Deposit Transaction Type")
    active = models.BooleanField(default=True)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id',)


class DepositTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.PROTECT,
                                     verbose_name="User Deposit Transactions",
                                     default=1,
                                     related_name='depositTransaction')
    payment_gateway = models.ForeignKey(PaymentGateway,
                                        on_delete=models.PROTECT,
                                        verbose_name="Payment Gateway Transactions",
                                        default=1,
                                        related_name='depositPaymentGateway')
    deposit_id = models.IntegerField(default=1)
    deposit_type = models.ForeignKey(DepositTransactionType,
                                     on_delete=models.PROTECT,
                                     verbose_name="Deposit Type of Transactions",
                                     default=1,
                                     related_name='depositTransactionType')
    deposit_status = models.ForeignKey(DepositTransactionStatus,
                                       on_delete=models.PROTECT,
                                       verbose_name="Deposit Status of Transactions",
                                       default=1,
                                       related_name='depositTransactionStatus')
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class WithdrawTransactionType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="NA", blank=False)
    active = models.BooleanField(default=True)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('name',)


class WithdrawTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.PROTECT,
                                     verbose_name="User Withdraw Transaction",
                                     default=1,
                                     related_name='withdrawTransaction')
    payment_gateway = models.ForeignKey(PaymentGateway,
                                        on_delete=models.PROTECT,
                                        verbose_name="Payment gateway of Withdraw Transaction",
                                        default=1,
                                        related_name='withdrawPaymentGateway')
    withdraw_id = models.IntegerField(default=1)
    withdraw_type = models.ForeignKey(WithdrawTransactionType,
                                      on_delete=models.PROTECT,
                                      verbose_name="Withdraw Type",
                                      default=1,
                                      related_name='withdrawTransactiontType')
    withdraw_status = models.ForeignKey(WithdrawTransactionStatus,
                                        on_delete=models.PROTECT,
                                        verbose_name="Withdraw Status",
                                        default=1,
                                        related_name='withdrawTransactionStatus')
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class DepositTransactionFees(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.PROTECT,
                                     verbose_name="User Deposit Transaction Fees",
                                     default=1,
                                     related_name='userDepositTransactionFees')
    house_fund = models.ForeignKey(HouseFund,
                                   on_delete=models.PROTECT,
                                   verbose_name='House Fund',
                                   default=1,
                                   related_name='depositHouseFund')
    payment_gateway = models.ForeignKey(PaymentGateway,
                                        on_delete=models.PROTECT,
                                        verbose_name='Deposit Gateway Fees',
                                        default=1,
                                        related_name='depositTransactionFeesPaymentGateway')
    deposit = models.ForeignKey(DepositTransaction,
                                on_delete=models.PROTECT,
                                verbose_name='Deposit Transaction Fees',
                                default=1,
                                related_name='depositTransactionFees')
    percentage_fee = models.FloatField(default=0.0, blank=False)
    flat_fee = models.FloatField(default=0.0, blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class WithdrawTransactionFees(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.PROTECT,
                                     verbose_name="User Withdraw Transaction Fees",
                                     default=1,
                                     related_name='userWithdrawTransactionFees')
    house_fund = models.ForeignKey(HouseFund,
                                   on_delete=models.PROTECT,
                                   verbose_name='House Fund',
                                   default=1,
                                   related_name='withdrawtHouseFund')
    payment_gateway = models.ForeignKey(PaymentGateway,
                                        on_delete=models.PROTECT,
                                        verbose_name='Withdraw Gateway Fees',
                                        default=1,
                                        related_name='withdrawTransactionFeesPaymentGateway')
    withdraw = models.ForeignKey(WithdrawTransaction,
                                 on_delete=models.PROTECT,
                                 verbose_name='Withdraw Transaction Fees',
                                 default=1,
                                 related_name='withdrawTransactionFees')
    percentage_fee = models.FloatField(default=0.0, blank=False)
    flat_fee = models.FloatField(default=0.0, blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class ZipCode(models.Model):
    id = models.AutoField(primary_key=True)
    zipcode = models.CharField(max_length=5, default="00000", blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.zipcode

    class Meta:
        ordering = ('zipcode',)


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    sort_name = models.CharField(max_length=3, verbose_name="2 letter name", blank=False, default="XX")
    name = models.CharField(max_length=30, verbose_name="Country Name", blank=False, default="XXX")
    phone_code = models.IntegerField(default=0, blank=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.sort_name

    class Meta:
        ordering = ('sort_name',)


class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, verbose_name="State Name", blank=False, default="XX")
    code = models.CharField(max_length=2, verbose_name="State Code", blank=False, default="XX")
    country = models.ForeignKey(Country, on_delete=models.PROTECT, default=1, verbose_name="State Country")
    zip_codes = models.ManyToManyField(ZipCode, default=1, related_name="zipcodesStates")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('name',)


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name="City Name", blank=False)
    state = models.ForeignKey(State, on_delete=models.PROTECT, default=1, verbose_name="State Country")
    zip_codes = models.ManyToManyField(ZipCode, default=1, related_name="citiesStates")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('name',)


class UserStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=ADDRESS_LENGTH, verbose_name="Status of User")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.status

    class Meta:
        ordering = ('id',)


class PasswordResetStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, verbose_name="Status of Password Reset")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.status

    class Meta:
        ordering = ('id',)


class NotificationType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, verbose_name="Type of Notification")
    active = models.BooleanField(default=False, verbose_name="Notification Type Active")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id',)


class NotificationStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, verbose_name="Status of Notification")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.status

    class Meta:
        ordering = ('id',)


class RegisterStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, verbose_name="Status of Register")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.status

    class Meta:
        ordering = ('id',)


class EmailAddressStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, verbose_name="Status of Email Address")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.status

    class Meta:
        ordering = ('id',)


class EmailAddressType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, verbose_name="Type of Email Address", blank=False, default="1")
    active = models.BooleanField(default=False, verbose_name="Email address Type Active")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id',)


class PhoneNumberType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, verbose_name="Type of Phone Number", blank=False, default="1")
    active = models.BooleanField(default=False, verbose_name="Phone Number Type Active")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id',)


class PhoneNumber(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.PROTECT,
                                     verbose_name="Phone Numbers",
                                     default=1,
                                     related_name='phoneNumbers')
    phone_number = models.CharField(max_length=16, default="0000000000", verbose_name="Phone Number")
    country = models.ForeignKey(Country,
                                on_delete=models.PROTECT,
                                verbose_name="Phone Number Country",
                                related_name='phoneNumberCountry',
                                default=1)
    type = models.ForeignKey(PhoneNumberType,
                             verbose_name="Phone Number Country",
                             on_delete=models.PROTECT,
                             related_name='phoneNumberType',
                             default=1)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.phone_number

    class Meta:
        ordering = ('id', 'phone_number', 'country',)


class NameType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=FIRST_NAME_LENGTH, verbose_name="Type of Name")
    active = models.BooleanField(default=False, verbose_name="Active Name Type")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id',)


class DocumentStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, verbose_name="Status of Document")
    active = models.BooleanField(default=False, verbose_name="Active Document Status")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.status

    class Meta:
        ordering = ('id', 'status',)


class DocumentType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, verbose_name="Type of Document")
    active = models.BooleanField(default=False, verbose_name="Active File Type")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', 'type',)


class FileType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, verbose_name="Type of Document")
    active = models.BooleanField(default=False, verbose_name="Active File Type")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('type',)


class MailServer(models.Model):
    id = models.AutoField(primary_key=True)
    vendor = models.CharField(max_length=255, blank=False, verbose_name="vendor name", default="No Name")
    username = models.CharField(max_length=EMAIL_LENGTH, blank=False, verbose_name="username", default="No Name")
    password = models.CharField(max_length=PASSWORD_LENGTH, blank=False, verbose_name="password", default="No Name")
    server = models.CharField(max_length=255, blank=False, verbose_name="server name", default="No Name")
    port = models.IntegerField(blank=False, default=465)
    active = models.BooleanField(default=False, verbose_name="Active Mail Server")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.vendor

    class Meta:
        ordering = ('vendor',)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/{1}/user_{2}/{3}'.format('2018', '03', instance.user.id, filename)


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, verbose_name="Filename of document", default="No Name")
    user = models.ForeignKey(UserProfile,
                             on_delete=models.CASCADE,
                             related_name="documenUser",
                             default=1)
    type = models.ForeignKey(DocumentType,
                             on_delete=models.CASCADE,
                             related_name="documentType",
                             default=1)
    document = models.FileField(upload_to=user_directory_path)
    file_type = models.ForeignKey(FileType, on_delete=models.CASCADE, default=1, related_name="documentFileType")
    size = models.IntegerField(blank=False, default=0)
    status = models.ForeignKey(DocumentStatus, on_delete=models.CASCADE, default=1, related_name="documentStatus")
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    modified = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id', 'type', 'document', 'user', 'status')


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, unique=True, editable=False)
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, default=1, related_name="customUser")
    email = models.EmailField(max_length=EMAIL_LENGTH,
                              blank=False,
                              verbose_name="Login of user",
                              unique=True)
    username = models.CharField(max_length=EMAIL_LENGTH,
                                blank=False,
                                verbose_name="username of user",
                                unique=True,
                                default="Username")
    status = models.ForeignKey(UserStatus, on_delete=models.CASCADE, default=1, related_name="customUserStatus",)
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    is_active = models.BooleanField(default=True)
    is_logged_in = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return '%s' % self.email

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [email]

    @staticmethod
    def get_full_name(self):
        self.full_name = '%s %s' % ("first", "last")
        return self.full_name.strip()

    @staticmethod
    def get_short_name():
        return "first"


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.PROTECT, verbose_name="Addresses", default=1,
                                     related_name='addressesUserProfile')
    address1 = models.CharField(max_length=255, verbose_name="Address 1", default="")
    address2 = models.CharField(max_length=255, verbose_name="Address 2", default="")
    address3 = models.CharField(max_length=255, verbose_name="Address 3", default="")
    unit = models.CharField(max_length=20, verbose_name="Unit", default="")
    zipcode = models.ForeignKey(ZipCode, on_delete=models.PROTECT, default=1, related_name='addressesZipcode')
    city = models.ForeignKey(City, on_delete=models.PROTECT, default=1, related_name='addressesCity')
    state = models.ForeignKey(State, on_delete=models.PROTECT, default=1, related_name='addressesState')
    country = models.ForeignKey(Country, on_delete=models.PROTECT, default=1, related_name='addressesCountry')
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class PasswordReset(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    authorization_code = models.CharField(max_length=AUTHORIZATION_CODE_LENGTH,
                                          blank=False,
                                          verbose_name="Password Reset Code")
    status = models.ForeignKey(PasswordResetStatus, on_delete=models.SET_DEFAULT, default=1)
    clicked = models.DateTimeField(auto_now=True, verbose_name="Time clicked")
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.user

    class Meta:
        ordering = ('id',)


class Network(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField(verbose_name="ID of Network", default=1)
    name = models.CharField(max_length=50, verbose_name="Name of Network", default='0')
    url = models.CharField(max_length=100, verbose_name="Url of Network", default='0')
    queryUrl = models.CharField(max_length=100, verbose_name="query Url of Network", default='0')
    api = models.CharField(max_length=ADDRESS_LENGTH, verbose_name="APIKey of Network", default='0')
    genesis = models.IntegerField(verbose_name="Beginning block Number", default=0)
    lastBlockChecked = models.IntegerField(verbose_name="Url of Network", default=0)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id',)


class Name(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.PROTECT, verbose_name="Names", default=1,
                                     related_name='names')
    name = models.CharField(max_length=FIRST_NAME_LENGTH, verbose_name="Name of User")
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    type = models.ForeignKey(NameType, on_delete=models.PROTECT, verbose_name="Name Type", default=1)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id',)


class EmailAddress(models.Model):
    id = models.AutoField(primary_key=True)
    user_profile = models.ForeignKey(UserProfile,
                                     on_delete=models.PROTECT,
                                     verbose_name="User Profile",
                                     default=1,
                                     related_name='emailAddresses')
    email = models.EmailField(max_length=EMAIL_LENGTH,
                              blank=False,
                              default='noemail@noemail.com',
                              verbose_name="Email of Register")
    type = models.ForeignKey(EmailAddressType, on_delete=models.CASCADE)
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    status = models.ForeignKey(EmailAddressStatus, on_delete=models.PROTECT, default=1)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.email

    class Meta:
        ordering = ('id',)


class EmailTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=60, verbose_name="Subject of Email")
    fromAddress = models.CharField(max_length=50, verbose_name="From Username")
    htmlFilename = models.FileField(upload_to=EMAIL_TEMPLATE_DIR,
                                    max_length=100,
                                    blank=True,
                                    null=True,
                                    verbose_name="Filename")
    textFilename = models.FileField(upload_to=EMAIL_TEMPLATE_DIR,
                                    max_length=100,
                                    blank=True,
                                    null=True,
                                    verbose_name="Filename")
    objects = models.Manager()

    @property
    def html_name(self):
        return self.htmlFilename.name

    @property
    def text_name(self):
        return self.textFilename.name

    def __str__(self):
        return '%s' % self.subject

    class Meta:
        ordering = ('id',)


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.ForeignKey(NotificationType, on_delete=models.SET_DEFAULT, default=1)
    fromUser = models.IntegerField(default=0)
    toUser = models.IntegerField(default=0)
    status = models.ForeignKey(NotificationStatus, on_delete=models.SET_DEFAULT, default=1)
    message = models.IntegerField(default=0)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.toUser

    class Meta:
        ordering = ('id',)


class Xchange(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    url = models.CharField(max_length=200, default="")
    category = models.CharField(max_length=50, default="")
    order = models.SmallIntegerField(default=1)
    api_url = models.CharField(max_length=200, default="")
    api_key = models.CharField(max_length=200, default="")
    api_secret = models.CharField(max_length=200, default="")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id',)


class NewsLetter(models.Model):
    email = models.EmailField(max_length=EMAIL_LENGTH, default="noemail@yogishouse.com", primary_key=True)
    timestamp = models.BigIntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.email

    class Meta:
        ordering = ('email', )


class Fund(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, unique=True)
    active = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class FundPeriod(models.Model):
    id = models.AutoField(primary_key=True)
    period = models.CharField(max_length=20, blank=False, default="Month")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class FundRebalanceDate(models.Model):
    id = models.AutoField(primary_key=True)
    num_of_coins = models.IntegerField(default=10)
    start_date = models.DateField()
    end_date = models.DateField()
    frequency = models.IntegerField(default=1)
    period = models.ForeignKey(FundPeriod,
                               on_delete=models.PROTECT,
                               default=1,
                               verbose_name="Repeat Period",
                               related_name="rebalancePeriod")
    fund = models.ForeignKey(Fund,
                             on_delete=models.PROTECT,
                             default=1,
                             verbose_name="Fund Rebalance Date",
                             related_name="FundRebalanceDateFund")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class FundCurrency(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.IntegerField(blank=True)
    fund = models.ForeignKey(Fund,
                             on_delete=models.PROTECT,
                             default=1,
                             verbose_name="Associated Fund",
                             related_name="associatedFund")
    rebalance = models.ForeignKey(FundRebalanceDate,
                                  on_delete=models.PROTECT,
                                  default=1,
                                  verbose_name="Rebalance Date of Fund",
                                  related_name="fundCurrencyRebalanceDate")
    rebalance_price = models.FloatField(default=0.0)
    market_cap = models.BigIntegerField(default=0)
    available_supply = models.BigIntegerField(default=0)
    percent = models.FloatField(default=0.0)
    amount = models.FloatField(default=0.0)
    rebalance_value = models.FloatField(default=0.0)
    end_price = models.FloatField(default=0.0)
    end_value = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)
    level = models.FloatField(default=0.0)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class Vendor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=50, default="")
    url = models.CharField(max_length=200, default="")
    api_url = models.CharField(max_length=200, default="")
    api_key = models.CharField(max_length=100, default="")
    username = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=50, default="")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id', 'name',)


class FundHistory(models.Model):
    id = models.AutoField(primary_key=True)
    fund = models.ForeignKey(Fund,
                             on_delete=models.SET_DEFAULT,
                             default=1,
                             verbose_name="History of Fund",
                             related_name="fundHistoryValues")
    time = models.DateField(verbose_name="Close Time")
    value = models.FloatField(default=0.0, verbose_name="Close Value")
    xchange = models.ForeignKey(Xchange,
                                on_delete=models.SET_DEFAULT,
                                default=1,
                                verbose_name="Xchange Used",
                                related_name="fundXchange")
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    objects = models.Manager()

    def __str__(self):
        return '%s:' % self.id

    class Meta:
        ordering = ('id',)


class UserAgent(models.Model):
    id = models.AutoField(primary_key=True)
    userAgent = models.CharField(max_length=255, blank=True, null=True, default='Unknown', verbose_name="User Agent")
    codeName = models.CharField(max_length=255, blank=True, null=True, default='Unknown', verbose_name="code Name")
    appName = models.CharField(max_length=255, blank=True, null=True, default='Unknown', verbose_name="app Name")
    appVersion = models.CharField(max_length=255, blank=True, null=True, default='Unknown', verbose_name="app Version")
    cookiesEnabled = models.BooleanField(default=True, verbose_name="cookies")
    language = models.CharField(max_length=30, blank=True, null=True, default='Unknown', verbose_name="language")
    platform = models.CharField(max_length=255, blank=True, null=True,
                                default='Unknown', verbose_name="platform")
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.appName

    class Meta:
        ordering = ('platform',)


class Affiliate(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=EMAIL_LENGTH,
                              blank=False,
                              default='noemail@noemail.com',
                              verbose_name="Email of Affiliate")
    firstName = models.CharField(max_length=FIRST_NAME_LENGTH, verbose_name="First Name of Affiliate")
    lastName = models.CharField(max_length=LAST_NAME_LENGTH, verbose_name="Last Name of Affiliate")
    zipCode = models.CharField(max_length=10, verbose_name="Zip Code of Affiliate", default="00000")
    phoneNumber = models.CharField(max_length=20, verbose_name="Phone Number of Affiliate", default="0000000000")
    companyName = models.CharField(max_length=LAST_NAME_LENGTH, verbose_name="Company Name of Affiliate")
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Date of Registration")
    status = models.ForeignKey(RegisterStatus, on_delete=models.PROTECT, default=1)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class Register(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=EMAIL_LENGTH,
                              blank=False,
                              default='noemail@noemail.com',
                              verbose_name="Email of Register")
    password = models.CharField(max_length=PASSWORD_LENGTH, verbose_name="Password of Register", default="none")
    firstName = models.CharField(max_length=FIRST_NAME_LENGTH, verbose_name="First Name of Register")
    lastName = models.CharField(max_length=LAST_NAME_LENGTH, verbose_name="Last Name of Register")
    zipCode = models.CharField(max_length=10, verbose_name="Zip Code of Register", default="00000")
    ipAddress = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP Address of Register")
    userAgent = models.ForeignKey(UserAgent, on_delete=models.CASCADE, default=1, verbose_name="User Agent of User")
    authorizationCode = models.CharField(max_length=AUTHORIZATION_CODE_LENGTH,
                                         blank=False,
                                         verbose_name="Auto Generated Auth Code")
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Date of Registration")
    status = models.ForeignKey(RegisterStatus, on_delete=models.PROTECT, default=1, verbose_name="Status of Registered User")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class ContactUsForm(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=EMAIL_LENGTH,
                              blank=False,
                              default='noemail@noemail.com',
                              verbose_name="Email")
    subject = models.CharField(max_length=50, verbose_name="Subject of email")
    name = models.CharField(max_length=LAST_NAME_LENGTH + FIRST_NAME_LENGTH, verbose_name="name of person")
    message = models.CharField(max_length=255, verbose_name="message")
    inserted = models.DateTimeField("Date of contact", auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.email

    class Meta:
        ordering = ('id',)
