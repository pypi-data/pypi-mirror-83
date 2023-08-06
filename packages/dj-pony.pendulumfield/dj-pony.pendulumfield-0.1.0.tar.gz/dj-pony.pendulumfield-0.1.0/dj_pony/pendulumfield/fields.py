import datetime
import pendulum
from django.core import exceptions
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from pendulum import DateTime
from pendulum.parsing.exceptions import ParserError
from dj_pony.pendulumfield import forms


class PendulumField(models.DateTimeField):
    """
    A date and time, including timezone information, represented in Python by a `pendulum.Pendulum` object.
    """

    description = _("A date and time, including timezone information")

    # noinspection PyMethodMayBeStatic
    def from_db_value(self, value, expression, connection, *args, **kwargs):
        if value is None:
            return value
        return pendulum.instance(value)

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

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return "" if value is None else value.isoformat()

    def pre_save(self, model_instance, add):
        value = super(PendulumField, self).pre_save(model_instance, add)
        if isinstance(value, datetime.datetime):
            value = pendulum.instance(value)
            setattr(model_instance, self.attname, value)
        return value

    def formfield(self, **kwargs):
        defaults = {"form_class": forms.PendulumField}
        defaults.update(kwargs)
        return super(PendulumField, self).formfield(**defaults)
