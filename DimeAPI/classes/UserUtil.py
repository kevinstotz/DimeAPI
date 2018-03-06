from django.core.exceptions import ObjectDoesNotExist
from DimeAPI.models import CustomUser
from DimeAPI.settings.base import AUTHORIZATION_CODE_LENGTH, PASSWORD_LENGTH
from random import randint, choice
import string
import logging

logger = logging.getLogger(__name__)


class UserUtils:
    def __init__(self):
        #  instance variable unique to each instance
        self.new_username = ""
        self.num_records = 1

    def find_username(self, username):

        while True:
            self.new_username = username + '_' + str(randint(100, 999))
            try:
                self.num_records = CustomUser.objects.get(username=username).count()
            except ObjectDoesNotExist:
                self.num_records = 0
                break

        return self.num_records


def get_user_from_email(email):
    try:
        customUser = CustomUser.objects.get(email=email)
        return customUser
    except ObjectDoesNotExist as error:
        print(error)
    return None


def get_authorization_code():
    letters = string.ascii_lowercase
    authorization_code = ''.join(choice(letters) for i in range(AUTHORIZATION_CODE_LENGTH))
    logger.debug(authorization_code)
    return authorization_code


def generate_password():
    letters = string.ascii_lowercase
    new_password = ''.join(choice(letters) for i in range(PASSWORD_LENGTH))
    result = 'Generated new Password:{0}'.format(new_password)
    logger.debug(result)
    return new_password


def get_client_ip(request):
    request.x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if request.x_forwarded_for:
        request.ip = request.x_forwarded_for.split(',')[0]
    else:
        request.ip = request.META.get('REMOTE_ADDR')
    return request.ip
