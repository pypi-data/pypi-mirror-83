from django.utils.translation import gettext_lazy as _
from django.forms import CharField, ValidationError
import datetime
import pendulum
from django.core import exceptions
from django.forms import DateTimeField
from django.utils import timezone
from pendulum import DateTime
from pendulum.parsing.exceptions import ParserError


class PendulumField(DateTimeField):
    def prepare_value(self, value):
        return value.to_datetime_string()

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, DateTime):
            return value
        if isinstance(value, datetime.datetime):
            return pendulum.instance(value)
        if isinstance(value, datetime.date):
            return pendulum.instance(
                datetime.datetime.combine(value, datetime.datetime.min.time())
            )
        try:
            return pendulum.parse(value, tz=timezone.get_current_timezone())
        except ParserError:
            raise exceptions.ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )

    def strptime(self, value, format):
        return pendulum.from_format(value, format, timezone.get_current_timezone())
