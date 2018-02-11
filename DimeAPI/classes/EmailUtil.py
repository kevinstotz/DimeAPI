from DimeAPI.models import EmailAddress, CustomUser

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class EmailUtil:

    def __init__(self):
        #  instance variable unique to each instance
        self.num_records = 1

    def find_email(self, email):

        try:
            self.num_records = EmailAddress.objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            self.num_records = 0
        except MultipleObjectsReturned:
            self.num_records = 1
            return self.num_records

        try:
            self.num_records = CustomUser.objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            self.num_records = 0
        except MultipleObjectsReturned:
            self.num_records = 1

        return self.num_records
