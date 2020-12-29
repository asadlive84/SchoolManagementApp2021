from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

import re


def validators_phone_number(number):
    number = str(number)
    phone = re.compile(r'([088]*)(0*){1}([1]{1}[4356789]{1})((\d){2})(\d{6}$)')

    try:
        phone.match(number).group()
        value = True
    except:
        value = False

    if not value:
        raise ValidationError(
            _('%(value)s is not valid mobile number'),
            params={'value': number},
        )
