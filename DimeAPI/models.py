from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from DimeAPI.settings.base import EMAIL_LENGTH, ADDRESS_LENGTH, FIRST_NAME_LENGTH, \
    LAST_NAME_LENGTH, AUTHORIZATION_CODE_LENGTH, EMAIL_TEMPLATE_DIR, CURRENCY_NAME_LENGTH, \
    COIN_SYMBOL_LENGTH, COIN_NAME_LENGTH, COIN_FULL_NAME_LENGTH, ICON_NAME_LENGTH, PASSWORD_LENGTH, AUTH_USER_MODEL
from .managers import UserManager
from DimeAPI.classes.UnixEpoch import UnixEpochDateTimeField
import datetime


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


class NameType(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=FIRST_NAME_LENGTH, verbose_name="Type of Name")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.type

    class Meta:
        ordering = ('id',)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=EMAIL_LENGTH,
                              blank=False,
                              verbose_name="Login of user",
                              unique=True)
    username = models.CharField(max_length=EMAIL_LENGTH,
                                blank=False,
                                verbose_name="username of user",
                                unique=True,
                                default="Username")
    status = models.ForeignKey(UserStatus, on_delete=models.CASCADE, default=1)
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    is_active = models.BooleanField(default=True)
    is_logged_in = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

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


class PasswordReset(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    authorizationCode = models.CharField(max_length=AUTHORIZATION_CODE_LENGTH,
                                         blank=False,
                                         verbose_name="Password Reset Code")
    status = models.ForeignKey(PasswordResetStatus, on_delete=models.SET_DEFAULT, default=1)
    clicked = models.DateTimeField(auto_now=True, verbose_name="Time clicked")
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.user.email

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
    name = models.CharField(max_length=FIRST_NAME_LENGTH, verbose_name="Name of User")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Login", default=1)
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")
    type = models.ForeignKey(NameType, on_delete=models.PROTECT, default=1)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id',)


class EmailAddress(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=EMAIL_LENGTH,
                              blank=False,
                              default='noemail@noemail.com',
                              verbose_name="Email of Register")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Login", default=1)
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
    api_key =  models.CharField(max_length=200, default="")
    api_secret =  models.CharField(max_length=200, default="")
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id',)


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=CURRENCY_NAME_LENGTH, default="")
    symbol = models.CharField(max_length=COIN_SYMBOL_LENGTH, default="")
    coinName = models.CharField(max_length=COIN_NAME_LENGTH, default="")
    fullName = models.CharField(max_length=COIN_FULL_NAME_LENGTH, default="")

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id',)


class CryptoCompareCoin(models.Model):
    xchange_coin = models.IntegerField(default=1)
    local_coin = models.OneToOneField(Currency, on_delete=models.CASCADE, primary_key=True, related_name='cryptoCompareCoin')
    xchange = models.ForeignKey(Xchange, on_delete=models.CASCADE)
    url = models.CharField(max_length=200, default="")
    image_url = models.CharField(max_length=200, default="")
    name = models.CharField(max_length=CURRENCY_NAME_LENGTH, default="")
    symbol = models.CharField(max_length=COIN_SYMBOL_LENGTH, default="")
    coin_name = models.CharField(max_length=COIN_NAME_LENGTH, default="")
    full_name = models.CharField(max_length=COIN_FULL_NAME_LENGTH, default="")
    algorithm = models.CharField(max_length=50, default="")
    proof_type = models.CharField(max_length=50, default="")
    fully_premined = models.SmallIntegerField(default=1)
    total_coin_supply = models.FloatField(default=0.0)
    pre_mined_value = models.CharField(max_length=20, default="")
    total_coins_free_float = models.CharField(max_length=20, default="")
    sort_order = models.SmallIntegerField(default=1)
    sponsored = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('name',)

class XchangeCurrency(models.Model):
    currencyXChange = models.ForeignKey(Xchange, on_delete=models.SET_DEFAULT, default=1)
    currency = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.currencyXChange

    class Meta:
        ordering = ('currencyXChange', 'currency')


class NewsLetter(models.Model):
    email = models.EmailField(default="noemail@thedime.fund", primary_key=True)
    timestamp = UnixEpochDateTimeField(allow_null=True)

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.email

    class Meta:
        ordering = ('email', )


class Period(models.Model):
    id = models.AutoField(primary_key=True)
    start_year = models.IntegerField(default=2017)
    start_month = models.IntegerField(default=1)
    start_day = models.IntegerField(default=1)
    end_year = models.IntegerField(default=2017)
    end_month = models.IntegerField(default=1)
    end_day = models.IntegerField(default=1)
    num_of_coins = models.IntegerField(default=10)

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
    api_key =  models.CharField(max_length=100, default="")
    username = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=50, default="")

    def __str__(self):
        return '%s' % self.name

    class Meta:
        ordering = ('id', 'name',)

class DimePeriod(models.Model):
    id = models.AutoField(primary_key=True)
    period = models.ForeignKey(Period, on_delete=models.SET_DEFAULT, default=1)
    currency = models.ForeignKey(Currency, on_delete=models.SET_DEFAULT, default=1)
    rank = models.SmallIntegerField(default=0)
    level = models.FloatField(default=0.0)
    rebalancePrice = models.FloatField(default=0.0)
    marketCap = models.BigIntegerField(default=0)
    percentOfDime = models.FloatField(default=0.0)
    amount = models.FloatField(default=0.0)
    rebalanceValue = models.FloatField(default=0.0)
    endPrice = models.FloatField(default=0.0)
    endValue = models.FloatField(default=0.0)
    objects = models.Manager()

    def __str__(self):
        return '%s: %s' % (self.period, self.currency)

    class Meta:
        ordering = ('id',)


class DimeMutualFund(models.Model):
    id = models.AutoField(primary_key=True)
    currency = models.ForeignKey(Currency, on_delete=models.SET_DEFAULT, default=1)
    rebalance_date = models.DateField(default=datetime.date.today)
    period = models.ForeignKey(Period, on_delete=models.SET_DEFAULT, default=1)
    rank = models.IntegerField(default=0)
    level = models.FloatField(default=0.0)
    rebalance_price = models.FloatField(default=0.0)
    market_cap = models.BigIntegerField(default=0)
    available_supply = models.BigIntegerField(default=0)
    percent_of_dime = models.FloatField(default=0.0)
    amount = models.FloatField(default=0.0)
    rebalance_value = models.FloatField(default=0.0)
    end_price = models.FloatField(default=0.0)
    end_value = models.FloatField(default=0.0)
    objects = models.Manager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        ordering = ('id',)


class DimeHistory(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.BigIntegerField(default=0, verbose_name="Close Date")
    value = models.FloatField(default=0.0)
    xchange = models.ForeignKey(Xchange, on_delete=models.SET_DEFAULT, default=1)
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Time inserted")

    objects = models.Manager()

    def __str__(self):
        return '%s: %s' % (self.id)

    class Meta:
        unique_together = (("time", "xchange"),)
        ordering = ('id',)


class UserAgent(models.Model):
    userAgent = models.CharField(max_length=255, blank=True, null=True, default='Unknown', verbose_name="User Agent")
    os = models.CharField(max_length=20, blank=True, null=True, default='Unknown', verbose_name="Operating System")
    browser = models.CharField(max_length=20, blank=True, null=True, default='Unknown', verbose_name="Browser")
    device = models.CharField(max_length=20, blank=True, null=True, default='Unknown', verbose_name="Device")
    os_version = models.CharField(max_length=30, blank=True, null=True, default='Unknown', verbose_name="OS Version")
    browser_version = models.CharField(max_length=30, blank=True, null=True,
                                       default='Unknown', verbose_name="OS Version")
    inserted = UnixEpochDateTimeField(default=0.0)

    objects = models.Manager()

    def __str__(self):
        return '%s' % self.userAgent

    class Meta:
        ordering = ('os',)


class Password(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=PASSWORD_LENGTH, verbose_name="Password")

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
    deviceInfo = models.ForeignKey(UserAgent, on_delete=models.CASCADE)
    authorizationCode = models.CharField(max_length=AUTHORIZATION_CODE_LENGTH,
                                         blank=False,
                                         verbose_name="Auto Generated Auth Code")
    inserted = models.DateTimeField(auto_now_add=True, verbose_name="Date of Registration")
    status = models.ForeignKey(RegisterStatus, on_delete=models.PROTECT, default=1)
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