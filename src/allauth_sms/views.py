from datetime import timedelta

from allauth.account.utils import perform_login
from allauth.socialaccount import app_settings
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import transaction
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import FormView

from .forms import LoginForm
from .models import OTP
from .provider import SMSProvider


class LoginView(FormView):
    template_name = "allauth_sms/login.html"
    form_class = LoginForm
    success_url = "/"

    @transaction.atomic
    def form_valid(self, form):
        if "code" in form.cleaned_data:
            # Verify code
            try:
                otp = OTP.objects.get(
                    phone=form.cleaned_data["phone"], code=form.cleaned_data["code"]
                )
            except OTP.DoesNotExist:
                form.add_error("code", "Entered code is invalid.")
                return super().form_invalid(form)
            if otp.is_used:
                form.add_error("code", "Entered code is already used.")
                return super().form_invalid(form)
            if otp.ctime < now() - timedelta(hours=1):
                form.add_error("code", "Entered code is expired.")
                return super().form_invalid(form)
            otp.is_used = True
            otp.save()
            # Find or create user for this phone
            try:
                account = SocialAccount.objects.get(
                    provider=SMSProvider.id, uid=otp.phone
                )
            except SocialAccount.DoesNotExist:
                user = User.objects.create(username=otp.phone)
                account = user.socialaccount_set.create(
                    provider=SMSProvider.id, uid=otp.phone
                )
            return perform_login(
                self.request,
                account.user,
                email_verification=app_settings.EMAIL_VERIFICATION,
            )
        else:
            # Prompt for code
            otp = form.save()
            otp.send()
            form = LoginForm(initial=form.cleaned_data, show_code=True)
            return super().form_invalid(form)
