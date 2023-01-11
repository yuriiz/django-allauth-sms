from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import Provider, ProviderAccount
from django.shortcuts import reverse


class SMSProvider(Provider):
    id = "sms"
    name = "SMS"

    def get_login_url(self, request, next=None, **kwargs):
        return reverse("account_login_sms")


provider_classes = [SMSProvider]
