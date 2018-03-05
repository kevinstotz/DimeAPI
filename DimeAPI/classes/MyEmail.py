from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta, datetime
import time
from DimeAPI.settings.base import \
    EMAIL_SERVER, \
    EMAIL_TEMPLATE_DIR, \
    NOTIFICATION_STATUS, \
    EMAIL_FROM_DOMAIN, \
    EMAIL_TEMPLATE, \
    EMAIL_LOGIN_URL, \
    NOTIFICATION_TYPE, \
    EMAIL_VERIFY_ACCOUNT_URL, \
    ENGINE_DOMAIN, \
    EMAIL_VERIFY_TRACK_URL, \
    EMAIL_ADDRESS_STATUS, \
    PASSWORD_RESET_URL, \
    PASSWORD_RESET_STATUS, \
    DASHBOARD_HOSTNAME_URL, \
    NAME_TYPE, \
    REGISTER_STATUS
from DimeAPI.models import \
    EmailTemplate, \
    Notification, \
    NotificationType, \
    NotificationStatus, \
    NameType, \
    Name, \
    CustomUser, \
    EmailAddress, \
    EmailAddressStatus, \
    PasswordResetStatus, \
    PasswordReset
from DimeAPI.models import RegisterStatus
from DimeAPI.classes import ReturnResponse, UserUtil
from os.path import join
import logging

logger = logging.getLogger(__name__)


class MyEmail:

    # class variable shared by all instances
    emailHost = ""
    emailPort = 0
    emailPassword = EMAIL_SERVER['PASSWORD']
    emailUsername = EMAIL_SERVER['USER']

    def __init__(self, name):
        #  instance variable unique to each instance
        self.name = name
        self.emailTemplate = ""
        self.subject = ""
        self.body = ""
        self.toEmail = ""
        self.fromEmail = ""

    def replace_string_in_template(self, search, replace):
        logger.debug('Searched:{0} Replaced:{1}'.format(search, replace))
        self.body = self.body.replace(search, replace)

    def load_template(self, template_filename):

        filename = join(EMAIL_TEMPLATE_DIR, template_filename)

        with open(filename, "r", encoding="utf8") as template:
            self.body = template.read()
        if len(self.body) > 10:
            result = 'Read Email Template:{0}'.format(filename)
            logger.debug(result)
            return ReturnResponse.Response(0, __name__, 'success', result).return_json()
        else:
            result = 'Failed Reading Email Template:{0}'.format(filename)
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

    def send_contact_us(self, contactus):

        try:
            email_template = EmailTemplate.objects.get(pk=EMAIL_TEMPLATE['CONTACTUS'])
            result = 'Getting  CONTACTUS :{0} from DB:'.format(email_template.htmlFilename)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed getting CONTACTUS record #:{0} from DB:'.format(EMAIL_TEMPLATE['CONTACTUS'])
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        notification = Notification()
        notification.toUser = 1
        notification.message = email_template.pk
        notification.type = NotificationType(pk=NOTIFICATION_TYPE['EMAIL'])

        try:
            self.load_template(email_template.htmlFilename.name)
            result = 'read email template file:{0}'.format(email_template.htmlFilename)
            logger.debug(result)
        except Exception as error:
            result = 'Failed reading Email template:{0}'.format(email_template.htmlFilename)
            logger.critical(result)
            logger.critical(error)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        self.subject = email_template.subject
        self.fromEmail = email_template.fromAddress + '@' + EMAIL_FROM_DOMAIN
        self.toEmail = email_template.fromAddress + '@' + EMAIL_FROM_DOMAIN
        self.replace_string_in_template('EMAIL_VERIFY_TRACK_URL',
                                        EMAIL_VERIFY_TRACK_URL + "contactus")
        self.replace_string_in_template('NAME', contactus.validated_data['name'] + " ")
        self.replace_string_in_template('EMAIL', contactus.validated_data['email'])
        self.replace_string_in_template('MESSAGE', contactus.validated_data['message'])

        if self.send() == 1:
            notification.status = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['SENT'])
            result = 'Contact us email sent to user ID:{0}'.format(contactus.validated_data['email'])
            logger.debug(result)
        else:
            notification.status = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['FAILED'])
            result = 'Failed sending email:{0} to user ID:{1}'.format(email_template.htmlFilename,
                                                                      contactus.validated_data['email'])
            logger.error(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()
        notification.save()
        result = 'Email sent!'
        return ReturnResponse.Response(0, __name__, 'success', result).return_json()


    def send_verify_email(self, register_user):

        try:
            email_template = EmailTemplate.objects.get(pk=EMAIL_TEMPLATE['VERIFY'])
            result = 'Getting EMAIL_TEMPLATE VERIFY :{0} from DB:'.format(email_template.htmlFilename)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed getting EMAIL_TEMPLATE record #:{0} from DB:'.format(EMAIL_TEMPLATE['VERIFY'])
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        notification = Notification()
        notification.toUser = register_user.pk
        notification.message = email_template.pk
        notification.type = NotificationType(pk=NOTIFICATION_TYPE['EMAIL'])

        try:
            self.load_template(email_template.htmlFilename.name)
            result = 'read email template file:{0}'.format(email_template.htmlFilename)
            logger.debug(result)
        except Exception as error:
            result = 'Failed reading Email template:{0}'.format(email_template.htmlFilename)
            logger.critical(result)
            logger.critical(error)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()

        self.subject = email_template.subject
        self.fromEmail = email_template.fromAddress + '@' + EMAIL_FROM_DOMAIN
        self.toEmail = register_user.email

        self.replace_string_in_template('EMAIL_VERIFY_TRACK_URL',
                                        EMAIL_VERIFY_TRACK_URL + register_user.authorizationCode)
        self.replace_string_in_template('EMAIL_VERIFY_ACCOUNT_URL',
                                        EMAIL_VERIFY_ACCOUNT_URL + register_user.authorizationCode)
        self.replace_string_in_template('FIRST_NAME', register_user.firstName + " ")
        self.replace_string_in_template('LAST_NAME', register_user.lastName)

        if self.send() == 1:
            notification.status = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['SENT'])
            register_user.status = RegisterStatus.objects.get(pk=REGISTER_STATUS['SENT'])
            register_user.save()
            result = 'Registered User and sent email to user ID:{0}'.format(register_user)
            logger.debug(result)
        else:
            notification.status = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['FAILED'])
            result = 'Failed sending email:{0} to user ID:{1}'.format(email_template.htmlFilename,
                                                                      register_user)
            logger.error(result)
            return ReturnResponse.Response(1, __name__, 'failed', result).return_json()
        notification.save()
        result = 'Verification email sent to:{}'.format(self.toEmail)
        return ReturnResponse.Response(0, __name__, 'success', result).return_json()


    def send_welcome_email(self, new_user, new_password):

        try:
            new_user = CustomUser.objects.get(pk=new_user.pk)
            result = 'Loaded New User in Users: Id:{0}'.format(new_user.pk)
            logger.debug(result)
        except ObjectDoesNotExist as error:
            result = 'Could not find New User in Users: Id:{0}'.format(new_user.pk)
            logger.error(result)
            logger.error(error)
            return ReturnResponse.Response(1, __name__, 'Could not find New User', result).return_json()

        try:
            email_template = EmailTemplate.objects.get(pk=EMAIL_TEMPLATE['WELCOME'])
            result = 'Loaded Email Template WELCOME:{0}'.format(email_template.htmlFilename)
            logger.debug(result)
        except ObjectDoesNotExist as error:
            result = 'Could not find Email Template:{0}'.format(error)
            logger.error(error)
            return ReturnResponse.Response(1, __name__, 'Could not find Email Template', result).return_json()

        notification = Notification()
        notification.toUser = new_user.pk
        notification.message = email_template.pk

        try:
            notification.type = NotificationType.objects.get(pk=NOTIFICATION_TYPE['EMAIL'])
            result = 'Loaded email type notification: Id:{0}'.format(NOTIFICATION_TYPE['EMAIL'])
            logger.debug(result)
        except ObjectDoesNotExist as error:
            result = 'Failed loading email type notification Type: {0}{1}'.format(NOTIFICATION_TYPE['EMAIL'], error)
            logger.error(error)
            logger.error(result)
            return ReturnResponse.Response(1, __name__, 'Failed loading email type notification', result).return_json()

        try:
            self.load_template(email_template.htmlFilenam.namee)
            result = 'read email template file:{0}'.format(email_template.htmlFilename)
            logger.debug(result)
        except Exception as error:
            result = 'Failed reading email template:{0}'.format(email_template.htmlFilename)
            logger.error(error)
            logger.error(result)
            return ReturnResponse.Response(1, __name__, 'Failed reading email template', result).return_json()

        self.subject = email_template.subject
        self.fromEmail = email_template.fromAddress + '@' + EMAIL_FROM_DOMAIN

        try:
            email_address_status = EmailAddressStatus.objects.get(pk=EMAIL_ADDRESS_STATUS['ACTIVE'])
            result = 'Loaded email address status Active: Id:{0}'.format(EMAIL_ADDRESS_STATUS['ACTIVE'])
            logger.debug(result)
        except ObjectDoesNotExist as error:
            result = 'Failed Loading email address status Active: Id:{0}'.format(EMAIL_ADDRESS_STATUS['ACTIVE'])
            logger.critical(error)
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'Failed Loading email address status', result).return_json()

        try:
            email_address = EmailAddress.objects.get(user=new_user, status=email_address_status)
            result = 'Loaded email address :{0}'.format(email_address.email)
            logger.debug(result)
        except ObjectDoesNotExist as error:
            result = 'Failed Loading email address:'
            logger.critical(result)
            logger.critical(error)
            return ReturnResponse.Response(1, __name__, 'Failed Loading email address', result).return_json()
        self.toEmail = email_address.email

        name_type = ""
        try:
            name_type = NameType.objects.get(pk=NAME_TYPE['FIRST'])
            result = 'Loaded name type:{0}'.format(name_type.type)
            logger.debug(result)
        except ObjectDoesNotExist:
            result = 'Failed Loading Name Type First:{0}'.format(name_type.type)
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'Failed Loading Name Type First', result).return_json()

        name = ""
        try:
            name = Name.objects.get(user=new_user, type=name_type)
            result = 'Loaded name:{0}'.format(name.name)
            logger.debug(result)
        except ObjectDoesNotExist as error:
            result = 'Loaded name type:{0}'.format(name.name)
            logger.critical(result)
            logger.critical(error)
            return ReturnResponse.Response(1, __name__, 'Failed Loading Name', result).return_json()

        self.subject = self.subject.replace('NAME', name.name)
        self.replace_string_in_template('PASSWORD', str(new_password))
        self.replace_string_in_template('USERNAME', email_address.email)
        self.replace_string_in_template('FIRST_NAME', name.name)
        self.replace_string_in_template('EMAIL_VERIFY_TRACK_URL', EMAIL_VERIFY_TRACK_URL)
        self.replace_string_in_template('DASHBOARD_HOSTNAME_URL', DASHBOARD_HOSTNAME_URL)

        if self.send() == 1:
            notification.status = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['SENT'])
            result = 'Welcome Email Sent to:{0}'.format(email_address.email)
            logger.debug(result)
        else:
            notification.status = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['FAILED'])
            result = 'Failed Welcome Email Sent to:{0}'.format(email_address.email)
            logger.info(result)
        notification.save()
        return ReturnResponse.Response(0, __name__, 'success', result).return_json()


    def send_forgot_password_email(self, user):

        try:
            password_reset = PasswordReset.objects.get(user=user)
            result = 'Loaded password reset for user Id:{0}'.format(user.pk)
            logger.debug(result)
        except ObjectDoesNotExist as error:
            password_reset = PasswordReset(user=user, status=PasswordResetStatus(PASSWORD_RESET_STATUS['ACTIVE']))

        password_reset.Clicked = time.time()
        password_reset.save()

        if password_reset.status == PASSWORD_RESET_STATUS['EXPIRED']:
            result = 'This Request has expired!  Click forgot password again.'
            logger.debug(result)
            return 'This Request has expired'

        if  (password_reset.inserted + timedelta(minutes=60)) <= datetime.now():
            password_reset.status = PasswordResetStatus(pk=PASSWORD_RESET_STATUS['EXPIRED'])
            password_reset.save()
            result = 'This Request has expired!  Click forgot password again.'
            logger.debug(result)
            return result

        if password_reset.status == PASSWORD_RESET_STATUS['CLICKED']:
            result = 'This Request has already been used!  Click forgot password again.'
            logger.debug(result)
            return 'This Request has already been used.'

        if password_reset.status == PASSWORD_RESET_STATUS['ACTIVE']:
            password_reset.status = PasswordResetStatus(pk=PASSWORD_RESET_STATUS['CLICKED'])
            password_reset.save()

        try:
            email_template = EmailTemplate.objects.get(pk=EMAIL_TEMPLATE['FORGOT'])
            result = 'Loaded email template FORGOT:{0}'.format(email_template.htmlFilename.name)
            logger.debug(result)
        except ObjectDoesNotExist as error:
            result = 'Failed Loading email template FORGOT ID{0}:'.format(EMAIL_TEMPLATE['FORGOT'])
            logger.critical(result)
            logger.critical(error)
            return 'Failed Loading email template FORGOT'

        notification = Notification()
        notification.toUser = user.pk
        notification.message = email_template.pk

        try:
            notification.type = NotificationType.objects.get(pk=NOTIFICATION_TYPE['EMAIL'])
            result = 'Loaded Notification type EMAIL:{0}'.format(NOTIFICATION_TYPE['EMAIL'])
            logger.debug(result)
        except ObjectDoesNotExist as error:
            result = 'Failed Loading Notification type EMAIL:{0}'.format(NOTIFICATION_TYPE['EMAIL'])
            logger.critical(result)
            logger.critical(error)
            return 'Failed Loading Notification type EMAIL'

        try:
            self.load_template(email_template.htmlFilename.name)
            result = 'read email template file:{0}'.format(email_template.htmlFilename)
            logger.debug(result)
        except Exception as error:
            result = 'Failed reading email template:{0}'.format(email_template.htmlFilename)
            logger.critical(result)
            logger.critical(error)
            return 'Failed reading email template'

        self.subject = email_template.subject
        self.fromEmail = email_template.fromAddress + '@' + EMAIL_FROM_DOMAIN
        self.toEmail = user.email

        try:
            name = Name.objects.get(user=user, type=NameType.objects.get(pk=NAME_TYPE['FIRST']))
            first_name = name.name
            result = 'Read User from DB:{0}'.format(first_name)
            logger.debug(result)
        except ObjectDoesNotExist as error:
            first_name = ""
            result = 'Failed reading user first name from DB UserId:{0}'.format(user.pk)
            logger.critical(result)
            logger.critical(error)
        self.subject = self.subject.replace('NAME', first_name)
        self.replace_string_in_template('PASSWORD_RESET_URL', PASSWORD_RESET_URL + password_reset.authorizationCode)

        if self.send() == 1:
            notification.status = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['SENT'])
            result = 'Forgot Password Email Sent to:{0}'.format(user.email)
            logger.debug(result)
        else:
            notification.status = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['FAILED'])
            result = 'Failed sending Forgot Password Email to:{0}'.format(user.email)
            logger.error(result)
        notification.save()
        return 'Password reset instruction sent'


    def send_reset_password_email(self, authorization_code):
        try:
            password_reset = PasswordReset.objects.get(authorizationCode=authorization_code)
            result = 'Read authorization code from DB:{0}'.format(authorization_code)
            logger.debug(result)
        except ObjectDoesNotExist as error:
            result = 'Failed Finding Authorization Code in Password Reset:{0}'.format(authorization_code)
            logger.info(result)
            logger.info(error)
            return ReturnResponse.Response(0, __name__, 'Failed Finding Authorization Code', result).return_json()

        if authorization_code != password_reset.authorizationCode:
            result = 'Codes do not match.  Request password again.:{0}<>{1}'.format(authorization_code,
                                                                                    password_reset.authorizationCode)
            logger.info(result)
            return ReturnResponse.Response(0, __name__, 'Invalid Code.  Request password again', result).return_json()

        if password_reset.Status.pk == PASSWORD_RESET_STATUS['FINISHED']:
            result = 'Already Used this request.  Request password again. ID:{0}'.format(password_reset.status.pk)
            logger.info(result)
            return ReturnResponse.Response(0, __name__, 'Request Used.  Request password again', result).return_json()

        password_reset.Clicked = time.time()
        password_reset.Status = PasswordResetStatus.objects.get(pk=PASSWORD_RESET_STATUS['FINISHED'])
        password_reset.save()

        try:
            email_template = EmailTemplate.objects.get(pk=EMAIL_TEMPLATE['RESET'])
            result = 'retrieve email template file:{0}'.format(email_template.htmlFilename)
            logger.debug(result)
        except ObjectDoesNotExist as error:
            result = 'Failed retrieving email RESET template:{0}'.format(EMAIL_TEMPLATE['RESET'])
            logger.critical(result)
            logger.critical(error)
            return ReturnResponse.Response(1, __name__, 'Failed retrieving email RESET', result).return_json()

        notification = Notification()
        notification.toUser = password_reset.user
        notification.message = email_template
        notification.type = NotificationType.objects.get(pk=NOTIFICATION_TYPE['EMAIL'])

        try:
            self.load_template(email_template.htmlFilename.name)
            result = 'read email template file:{0}'.format(email_template.htmlFilename.name)
            logger.debug(result)
        except Exception as error:
            result = 'Failed reading email template:{0}'.format(email_template.htmlFilename)
            logger.critical(error)
            logger.critical(result)
            return ReturnResponse.Response(1, __name__, 'Failed reading email template', result).return_json()

        self.subject = email_template.subject
        self.fromEmail = email_template.fromAddress + '@' + EMAIL_FROM_DOMAIN

        try:
            user = CustomUser.objects.get(pk=password_reset.user.pk)
            result = 'Read email address from user:{0}'.format(user.email)
            logger.debug(result)
        except ObjectDoesNotExist as error:
            result = 'Failed reading user email address from User ID:{0}'.format(password_reset.user)
            logger.critical(result)
            logger.critical(error)
            return ReturnResponse.Response(1, __name__, 'No email address found', result).return_json()

        self.toEmail = user.email

        try:
            name = Name.objects.get(user=user.pk, type=NameType.objects.get(pk=NAME_TYPE['FIRST']))
            first_name = name.Name
            result = 'Read user id and first name from password reset:{0}'.format(name.pk)
            logger.debug(result)
        except ObjectDoesNotExist as error:
            first_name = ""
            result = 'Failed reading user id and first name from password reset:{0}'.format(user.pk)
            logger.error(result)
            logger.critical(error)

        utils = UserUtil.Util()
        new_password = utils.generate_password()
        user.set_password(new_password)
        user.save()
        self.replace_string_in_template('NEW_PASSWORD', str(new_password))
        self.subject = self.subject.replace('NAME', first_name)
        self.replace_string_in_template('EMAIL_LOGIN_URL', str(EMAIL_LOGIN_URL))
        if self.send() == 1:
            notification.status = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['SENT'])
            result = 'Reset Password Email Sent to:{0}'.format(user.email)
            logger.debug(result)
        else:
            notification.status = NotificationStatus.objects.get(pk=NOTIFICATION_STATUS['FAILED'])
            result = 'Failed sending Reset Password Email to:{0}'.format(user.email)
            logger.error(result)
        notification.save()
        return ReturnResponse.Response(0, __name__, 'Reset Password Email Sent', result).return_json()

    def send(self):
        return send_mail(
            self.subject,
            "txt version",
            self.fromEmail,
            [self.toEmail],
            html_message=self.body,
            auth_user=self.emailUsername,
            auth_password=self.emailPassword,
            fail_silently=False)
