from random import randint

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from sms import send_sms


def generate_code():
    return randint(100_000, 999_999)


class OTP(models.Model):
    phone = PhoneNumberField()
    ctime = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=6, default=generate_code)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return str(self.code)

    def send(self):
        send_sms(
            "Your verification code: " + str(self.code),
            None,
            [str(self.phone)],
            fail_silently=False,
        )
