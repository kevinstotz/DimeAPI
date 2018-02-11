from django.core.exceptions import ValidationError
from rest_framework import serializers
from datetime import datetime, timedelta, tzinfo
import datetime
import calendar


class GMT1(tzinfo):

    def utcoffset(self, dt):
        return timedelta(hours=1) + self.dst(dt)

    def dst(self, dt):
        # DST starts last Sunday in March
        d = datetime.datetime(dt.year, 4, 1)   # ends last Sunday in October
        self.dston = d - timedelta(days=d.weekday() + 1)
        d = datetime.datetime(dt.year, 11, 1)
        self.dstoff = d - timedelta(days=d.weekday() + 1)
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return timedelta(hours=1)
        else:
            return timedelta(0)

    def tzname(self, dt):
        return "GMT +1"


class UnixEpochDateTimeField(serializers.DateTimeField):
    def to_native(self, value):
        """
        to_native method is responsible for turning the
        Python object into a simple, serializable value.
        Here: return epoch time for a datetime object or `None`
        """
        return datetime_to_epoch(value)

    def from_native(self, value):
            return self.epoch_to_datetime(value)

    @staticmethod
    def epoch_to_datetime(value):
        try:
            return datetime.datetime.utcfromtimestamp(int(value)).replace(tzinfo=GMT1())
        except (ValueError, TypeError):
            raise ValidationError('%s is not a valid value' % value)


class UnixEpochDateField(serializers.DateField):
    def to_native(self, value):
        return self.date_to_epoch(value)

    def from_native(self, value):
            return self.epoch_to_date(value)

    @staticmethod
    def date_to_epoch(value):
        try:
            return int(calendar.timegm(value.timetuple()))
        except (AttributeError, TypeError):
            return None

    @staticmethod
    def epoch_to_date(value):
        try:
            return datetime.date.fromtimestamp(int(value))
        except (ValueError, TypeError):
            raise ValidationError('%s is not a valid value' % value)

def datetime_to_epoch(value):
    try:
        return int(calendar.timegm(value.utctimetuple()))
    except (AttributeError, TypeError):
        return None